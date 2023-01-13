import json
import os
import sys
import threading
import random

import pandas as pd

from sklearn.model_selection import train_test_split

from segregation_system.Objects import DataExtractor
from segregation_system.Objects.CommunicationController import CommunicationController, send_to_testing_system
from segregation_system.Objects.DBHandler import DBHandler
from segregation_system.Objects.SegregationSystemConfiguration import SegregationSystemConfiguration
from segregation_system.Objects.ResponseExtractor import ResponseExtractor
from segregation_system.Objects.Plotters import PlotterHistogram, PlotterRadarDiagram

PATH_DB = "./database/segregationSystemDatabase.db"
BALANCING_REPORT_PATH = "./graphs/Balancing_plot.png"
QUALITY_REPORT_PATH = "./graphs/radar_diagram.png"

TESTING_PHASE = True
SERVER_STARTED = False
TEST_RUN_NR = 0
TEST_SESSIONS_PER_RUN = [50, 100, 200, 300, 400, 500]


class SegregationSystemController:
    """
    Class that manage all the logic inside the Segregation System
    """

    def __init__(self):
        self.config_file = SegregationSystemConfiguration()
        self.db_handler = DBHandler(PATH_DB)
        self.lock = threading.RLock()
        self.mode = 0
        self.sessions_nr = 0
        self.semaphore = threading.Semaphore(0)

    def check_balancing(self):
        """
        Method that calls the API that extracts the data
        and plot them in order to evaluate the data balancing
        :return: Null
        """

        data_extractor = DataExtractor.DataExtractor(self.db_handler)
        labels = data_extractor.count_labels()

        plotter = PlotterHistogram(labels)
        plotter.plot_data_balancing()

        # The system now needs to stop, we need to wait the Data Analyst evaluation
        if TESTING_PHASE:
            random_number = random.randint(0, 9)
            # Set as 20% failure, 80% success
            if random_number >= 8:
                with open('./responses/balancing_response.json', 'r', encoding='utf-8') as opened_file:
                    data = json.load(opened_file)
                    data['response'] = 'No'
                with open('./responses/balancing_response.json', 'w', encoding='utf-8') as response:
                    json.dump(data, response)
            else:
                with open('./responses/balancing_response.json', 'r', encoding='utf-8') as opened_file:
                    data = json.load(opened_file)
                    data['response'] = 'Yes'
                with open('./responses/balancing_response.json', 'w', encoding='utf-8') as response:
                    json.dump(data, response)
            return
        # Bypass if testing is set
        sys.exit(0)

    def check_quality(self):
        """
        Method that calls the API that extracts the data
        and plot them in order to evaluate the data quality
        """

        data_extractor = DataExtractor.DataExtractor(self.db_handler)
        data = data_extractor.extract_features()

        plotter = PlotterRadarDiagram(data)
        plotter.plot_data_quality()

        # The system now needs to stop, we need to wait the Data Analyst evaluation
        if TESTING_PHASE:
            random_number = random.randint(0, 9)
            # Set as 20% failure, 80% success
            if random_number >= 2:
                with open('./responses/quality_response.json', 'r', encoding='utf-8') as opened_file:
                    data = json.load(opened_file)
                    data['response'] = 'No'
                with open('./responses/quality_response.json', 'w', encoding='utf-8') as response:
                    json.dump(data, response)
            else:
                with open('./responses/quality_response.json', 'r', encoding='utf-8') as opened_file:
                    data = json.load(opened_file)
                    data['response'] = 'Yes'
                with open('./responses/quality_response.json', 'w', encoding='utf-8') as response:
                    json.dump(data, response)
            return
        # Bypass if testing is set
        sys.exit(0)

    def generate_datasets(self):
        """
        Method that manage the flow of the final phase, extracts data from the DB
        and splits them in train, validation and test sets
        """

        data_extractor = DataExtractor.DataExtractor(self.db_handler)
        data_frame_input = data_extractor.extract_all()

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
        # Set data type
        x_train['type'] = 0         # train type
        x_validation['type'] = 1    # validation type
        x_test['type'] = 2          # test type

        # concatenate input and output
        x_train['label'] = y_train['label']
        x_validation['label'] = y_validation['label']
        x_test['label'] = y_test['label']

        res = pd.concat([x_train, x_validation, x_test], ignore_index=True)

        # Update the type and mark the records as used
        self.db_handler.update_type()

        communication_controller = CommunicationController(self.db_handler,
                                                           self.config_file.development_system_url,
                                                           self)
        communication_controller.send_datasets(res.to_dict())
        print("Dataset sent, now terminate")

        # remove the generated graphs
        try:
            os.remove(BALANCING_REPORT_PATH)
            os.remove(QUALITY_REPORT_PATH)
        except FileNotFoundError as ex:
            print(f"Error during file removal: {ex}")
        # reset the mode to accept more data from now on
        with self.lock:
            self.mode = 0

        # New testing phase
        if TESTING_PHASE:
            return

        sys.exit(0)

    def check_response(self):
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
        global SERVER_STARTED

        extractor = ResponseExtractor()

        # Start the Flask server on a daemon thread
        communication_controller = \
            CommunicationController(self.db_handler,
                                    self.config_file.development_system_url,
                                    self)
        flask_thread = threading.Thread(target=communication_controller.init_rest_server,
                                        daemon=True)
        flask_thread.start()

        while True:
            result_balancing = extractor.extract_json_response_balancing()
            # If the value is different from None the Analyst has evaluated the balancing histogram
            if result_balancing not in ['None', 'none']:
                if result_balancing in ['yes', 'Yes']:
                    self.check_quality()
                elif result_balancing in ['no', 'No']:
                    print('Negative response: send a configuration request to'
                          ' System Administrator for balancing problems')
                    if TESTING_PHASE:
                        send_to_testing_system(1)
                        continue
                else:
                    print('Unknown response: please write "yes" or "no" inside the file')
                if not TESTING_PHASE:
                    sys.exit(0)

            result_quality = extractor.extract_json_response_quality()

            # If the value is different from None the Analyst has evaluated the radar diagram
            if result_quality not in ['None', 'none']:
                if result_quality in ['yes', 'Yes']:
                    self.generate_datasets()
                elif result_quality in ['no', 'No']:
                    print('Negative response: send a configuration request to'
                          ' System Administrator for quality problems')
                    if TESTING_PHASE:
                        send_to_testing_system(2)
                        continue
                else:
                    print('Unknown response: please write "yes" or "no" inside the file')

            self.semaphore.acquire()
            self.check_balancing()

    def manage_message(self, file_json):
        """
        Function that manage the flow after receiving a message from preparation system
        :param file_json: arrived data
        :return: None
        """
        global TEST_RUN_NR

        # If our system is involved with data balancing and quality I cannot
        # accept more prepared sessions so the system discards them
        with self.lock:
            if self.mode == 1:
                return

            self.db_handler.create_arrived_session_table()

            # Instantiate a data frame
            data_frame = pd.DataFrame(file_json,
                                      columns=['id', 'time_mean', 'time_median', 'time_std',
                                               'time_kurtosis', 'time_skewness', 'amount_mean',
                                               'amount_median', 'amount_std', 'amount_kurtosis',
                                               'amount_skewness', 'type', 'label'])

            ret = self.db_handler.insert_session(data_frame)

            # if we received 7 sessions the system can continue its execution,
            # otherwise it will terminate waiting for a new message
            if not ret:
                return
            self.sessions_nr += 1
            print(self.sessions_nr)
            if not TESTING_PHASE:
                if self.sessions_nr != self.config_file.session_nr_threshold:
                    sys.exit(0)
            else:
                if self.sessions_nr != TEST_SESSIONS_PER_RUN[TEST_RUN_NR]:
                    sys.exit(0)
            self.sessions_nr = 0
            self.mode = 1
            TEST_RUN_NR += 1
        self.semaphore.release()
