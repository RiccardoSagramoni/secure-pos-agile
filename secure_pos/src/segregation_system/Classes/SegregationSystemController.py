import os
import sys
import json
from threading import Semaphore

import pandas as pd

from sklearn.model_selection import train_test_split

from segregation_system.Classes.DataExtractor import DataExtractor
from segregation_system.Classes.SegregationSystemConfiguration import SegregationSystemConfiguration
from segregation_system.utility.extract_json_response import extract_json_response
from src.communication import RestServer
from src.communication.api.file_transfer import ReceiveFileApi
from src.database import DBManager
from segregation_system.utility.plotter import plot_data_quality, plot_data_balancing

CONFIGURATION_PATH = 'segregation_configuration.json'
CONFIGURATION_SCHEMA_PATH = 'segregation_configuration_schema.json'


class SegregationSystemController:
    """
    Class that manage all the logic inside the Segregation System
    """

    def __init__(self):
        self.sessions_nr = 0
        self.path_db = "./database/segregationSystemDatabase.db"
        self.filename = './database/PreparedSession.json'
        self.data_balancing_response = './responses/balancing_response.json'
        self.data_quality_response = './responses/quality_response.json'
        self.mode_semaphore = Semaphore()
        self.mode = 0
        self.config_file = SegregationSystemConfiguration(CONFIGURATION_PATH,
                                                          CONFIGURATION_SCHEMA_PATH)
        self.check_file_existence()

    def handle_message(self):
        """
        Method that handle the incoming messages (preparation system)
        """
        # If our system is involved with data balancing and quality I cannot accept more prepared sessions
        # so the system discards them
        if self.mode == 1:
            os.remove(self.filename)
            sys.exit(0)

        # Store the information inside the local database
        data_base_manager = DBManager.DBManager(self.path_db)

        # If this is the first execution we have to create our table
        data_base_manager.create_table(
            "CREATE TABLE IF NOT EXISTS ArrivedSessions"
            "(id INT PRIMARY KEY UNIQUE, time_mean FLOAT, time_std FLOAT, time_skew FLOAT,"
            "amount_1 FLOAT, amount_2 FLOAT, amount_3 FLOAT, amount_4 FLOAT, amount_5 FLOAT,"
            "amount_6 FLOAT, amount_7 FLOAT, amount_8 FLOAT, amount_9 FLOAT, amount_10 FLOAT,"
            "type INT, label INT)")

        # Insert the record inside the table
        with open(self.filename, 'r', encoding='utf-8') as opened_file:
            data = json.load(opened_file)

        # Error checking
        if not data:
            print("Error during message receiving, data not found.")
            sys.exit(-1)

        # Instantiate a data frame
        data_frame = pd.DataFrame(data,
                                  columns=['id', 'time_mean', 'time_std', 'time_skew',
                                           'amount_1', 'amount_2', 'amount_3', 'amount_4',
                                           'amount_5', 'amount_6', 'amount_7', 'amount_8',
                                           'amount_9', 'amount_10', 'type', 'label'])

        # TODO: dealing with multithreading we need a
        #  semaphore to access the database
        ret = data_base_manager.insert(data_frame, 'ArrivedSessions')
        # os.remove(self.filename)

        # if we received 7 sessions the system can continue its execution,
        # otherwise it will terminate waiting for a new message
        if ret:
            self.sessions_nr += 1
            if self.sessions_nr == 7:
                self.sessions_nr = 0
                self.mode_semaphore
                self.mode = 1
                self.check_balancing()

    def server_start(self):
        """
        Method that create the server waiting for prepared sessions
        """
        # The first step is to manage all the sessions that the
        # Preparation system will send and wait until a sufficient amount of sessions are arrived

        # Instantiate server
        server = RestServer()
        server.api.add_resource(ReceiveFileApi,
                                "/",
                                resource_class_kwargs={'filename': self.filename,
                                                       'handler': self.handle_message()})
        server.run(debug=True)
        sys.exit(0)

    def check_balancing(self):
        """
        Method that calls the API that extracts the data
        and plot them in order to evaluate the data balancing
        :return: Null
        """
        data_extractor = DataExtractor(self.path_db)
        labels = data_extractor.count_labels()

        plot_data_balancing(labels)

        # The system now needs to stop, we need to wait the Data Analyst evaluation
        sys.exit(0)

    def check_quality(self):
        """
        Method that calls the API that extracts the data
        and plot them in order to evaluate the data quality
        """
        data_extractor = DataExtractor(self.path_db)
        data = data_extractor.extract_features()

        plot_data_quality(data)

        # The system now needs to stop, we need to wait the Data Analyst evaluation
        sys.exit(0)

    def generate_datasets(self):
        """
        Method that manage the flow of the final phase, extracts data from the DB
        and splits them in train, validation and test sets
        """
        data_extractor = DataExtractor(self.path_db)
        data_frame_input = data_extractor.extract_features()

        data_frame_result = data_extractor.extract_labels()

        # Splitting the data into 'train' and 'other',
        # aiming for 70% train 15% validation and 15% test
        x_train, x_other, y_train, y_other = train_test_split(data_frame_input,
                                                              data_frame_result,
                                                              stratify=data_frame_result,
                                                              test_size=0.3)

        x_validation, x_test, y_validation, y_test = train_test_split(x_other,
                                                                      y_other,
                                                                      stratify=y_other,
                                                                      test_size=0.5)


        # Mark the records as USED TODO remove comment below
        # database.update("UPDATE ArrivedSessions SET type = 0 WHERE type = -1")
        print("Dataset sent, now terminate")
        # reset the mode to accept more data from now on
        self.mode = 0
        sys.exit(0)

    def check_file_existence(self):
        """
        Function that checks which phase we need to execute, three options are available:
        - First start:  The REST server is not started yet, so we need to start it waiting for
                        new incoming messages from Preparation system.

        - Check data balancing: The system has received enough sessions in order to generate the
                        balancing histogram, it suspended its execution waiting for the Data Analyst
                        to check if the data are correctly balanced

        -Check data quality: The Data Analyst has evaluated the data as "Balanced" and the system
                        continued its execution until the radar diagram has been generated, the
                        system suspended again waiting for the Data Analyst response
        """

        result_balancing = extract_json_response(self.data_balancing_response)

        # If the value is different from None the Analyst has evaluated the balancing histogram
        if result_balancing not in ['None', 'none']:
            if result_balancing in ['yes', 'Yes']:
                self.check_quality()
            elif result_balancing in ['no', 'No']:
                print('Negative response: send a configuration request to'
                      ' System Administrator for balancing problems')
            else:
                print('Unknown response: please write "yes" or "no" inside the file')
            sys.exit(0)

        result_quality = extract_json_response(self.data_quality_response)

        # If the value is different from None the Analyst has evaluated the radar diagram
        if result_quality not in ['None', 'none']:
            if result_quality in ['yes', 'Yes']:
                self.generate_datasets()
            elif result_quality in ['no', 'No']:
                print('Negative response: send a configuration request to'
                      ' System Administrator for quality problems')
            else:
                print('Unknown response: please write "yes" or "no" inside the file')

        # If nothing has been set means that the rest server has to be started
        self.server_start()
