import os
import sys
import json
import pandas as pd

from src.segregation_system.Classes.DataStatsExtractor import DataStatsExtractor
from src.communication import RestServer
from src.communication.api.file_transfer import ReceiveFileApi
from src.database import DBManager
from src.segregation_system.Classes.Plotter import Plotter


def extract_json_response(file) -> object:
    """
    Function that extract the Data Analyst response from the file
    :param file: path of the file to be checked
    :return: string containing the response
    """
    if os.path.exists(file):
        with open(file, 'r+', encoding='utf-8') as file_opened:
            data = json.load(file_opened)
            result = data.pop('response')
            #data['response'] = 'None'

            # Rewind needed for overwriting and reset the variable
            #file_opened.seek(0)
            #json.dump(data, file_opened)
            #file_opened.truncate()
    return result


class SegregationSystemController:
    """
    Class that manage all the logic inside the Segregation System
    """

    def __init__(self):
        self.sessions_nr = 0
        self.path_db = "./database/segregationSystemDatabase.db"
        self.filename = 'PreparedSession.json'
        self.data_balancing_response = 'responses/balancing_response.json'
        self.data_quality_response = 'responses/quality_response.json'
        self.mode = 0

        # Needed for testing, TODO remove them
        self.check_file_existence()

    def handle_message(self):
        """
        Method that handle the messages arrived from the preparation system
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
        data_frame = pd.DataFrame(data,
                                  columns=['id', 'time_mean', 'time_std', 'time_skew', 'amount_1', 'amount_2',
                                           'amount_3', 'amount_4', 'amount_5', 'amount_6', 'amount_7', 'amount_8',
                                           'amount_9', 'amount_10', 'type', 'label'])

        num_rows = len(data_frame.index)

        # TODO dealing with multithreading we need a semaphore to access the database
        ret = data_base_manager.insert(data_frame, 'ArrivedSessions')
        # os.remove(self.filename)

        # if we received 7 sessions the system can continue its execution,
        # otherwise it will terminate waiting for a new message
        if ret:
            self.sessions_nr += num_rows
            if self.sessions_nr == 7:
                self.sessions_nr = 0
                # Refuse more Prepared sessions TODO Semaphore needed
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
                                                       'handler': lambda: self.handle_message()})
        server.run(debug=True)
        sys.exit(0)

    def check_balancing(self):
        """
        Method that calls the API that extracts the data
        and plot them in order to evaluate the data balancing
        :return: Null
        """
        data_extractor = DataStatsExtractor(self.path_db)
        labels = data_extractor.count_labels()
        value_0 = labels.pop(0).values[0][0]
        value_1 = labels.pop(0).values[0][0]

        plotter = Plotter()
        plotter.plot_data_balancing([value_0, value_1])

        # The system now needs to stop, we need to wait the Data Analyst evaluation
        sys.exit(0)

    def check_quality(self):
        """
        Method that calls the API that extracts the data
        and plot them in order to evaluate the data quality
        """

        data_extractor = DataStatsExtractor(self.path_db)
        data = data_extractor.extract_radar_diagram_data()

        plotter = Plotter()
        plotter.plot_data_quality(data)

        # The system now needs to stop, we need to wait the Data Analyst evaluation
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
                self.check_quality()
            elif result_quality in ['no', 'No']:
                print('Negative response: send a configuration request to'
                      ' System Administrator for quality problems')
            else:
                print('Unknown response: please write "yes" or "no" inside the file')

        sys.exit(0)
