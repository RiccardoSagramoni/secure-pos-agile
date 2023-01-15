import json
import os
import sys
import threading
import random

import pandas as pd

from sklearn.model_selection import train_test_split

import utility
from segregation_system.data_extractor import DataExtractor
from segregation_system.communication_controller import CommunicationController, send_to_testing_system
from segregation_system.db_handler import DBHandler
from segregation_system.segregation_system_configuration import SegregationSystemConfiguration
from segregation_system.response_extractor import ResponseExtractor
from segregation_system.plotters import PlotterHistogram, PlotterRadarDiagram

PATH_DB = "segregation_system/database/segregationSystemDatabase.db"
BALANCING_REPORT_PATH = "segregation_system/graphs/Balancing_plot.png"
QUALITY_REPORT_PATH = "segregation_system/graphs/radar_diagram.png"

TESTING_PHASE = True
TESTING_DB_RESET = [5, 10, 15, 20, 25]
TESTING_ITER = 0


class SegregationSystemController:
    """
    Class that manage all the logic inside the Segregation System
    """
    current_iteration = 0
    server_started = False

    def __init__(self):
        self.config_file = SegregationSystemConfiguration()
        self.db_handler = DBHandler(PATH_DB)
        self.lock = threading.RLock()
        self.sessions_nr = 0
        self.semaphore = threading.Semaphore(0)

    def check_balancing(self):
        """
        Method that calls the API that extracts the data
        and plot them in order to evaluate the data balancing
        :return: Null
        """
        global TESTING_ITER

        data_extractor = DataExtractor(self.db_handler,
                                       self.current_iteration,
                                       self.config_file.session_nr_threshold)
        labels = data_extractor.count_labels()

        plotter = PlotterHistogram(labels)
        plotter.plot_data_balancing()

        if not TESTING_PHASE:
            sys.exit(0)

        # The system now needs to stop, we need to wait the Data Analyst evaluation
        random_number = random.randint(0, 9)
        # Set as 20% failure, 80% success
        if random_number >= 8:
            self.current_iteration += 1
            if self.current_iteration == TESTING_DB_RESET[TESTING_ITER]:
                self.db_handler.drop_db()
                TESTING_ITER = (TESTING_ITER + 1) % 5
                self.current_iteration = 0
            with open(os.path.join(
                    utility.data_folder, 'segregation_system/responses/balancing_response.json'),
                    'r',
                    encoding='utf-8') as opened_file:
                data = json.load(opened_file)
                data['response'] = 'No'
            with open(os.path.join(
                    utility.data_folder, 'segregation_system/responses/balancing_response.json'),
                    'w',
                    encoding='utf-8') as response:
                json.dump(data, response)
        else:
            with open(os.path.join(
                    utility.data_folder, 'segregation_system/responses/balancing_response.json'),
                    'r',
                    encoding='utf-8') as opened_file:
                data = json.load(opened_file)
                data['response'] = 'Yes'
            with open(os.path.join(
                    utility.data_folder, 'segregation_system/responses/balancing_response.json'),
                    'w',
                    encoding='utf-8') as response:
                json.dump(data, response)

    def check_quality(self):
        """
        Method that calls the API that extracts the data
        and plot them in order to evaluate the data quality
        """
        global TESTING_ITER
        data_extractor = DataExtractor(self.db_handler,
                                       self.current_iteration,
                                       self.config_file.session_nr_threshold)
        data = data_extractor.extract_features()

        plotter = PlotterRadarDiagram(data)
        plotter.plot_data_quality()

        if not TESTING_PHASE:
            sys.exit(0)

        # The system now needs to stop, we need to wait the Data Analyst evaluation
        random_number = random.randint(0, 9)
        # Set as 20% failure, 80% success
        if random_number >= 8:
            self.current_iteration += 1
            if self.current_iteration == TESTING_DB_RESET[TESTING_ITER]:
                self.db_handler.drop_db()
                TESTING_ITER = (TESTING_ITER + 1) % 5
                self.current_iteration = 0
            with open(os.path.join(
                    utility.data_folder, 'segregation_system/responses/quality_response.json'),
                    'r',
                    encoding='utf-8') as opened_file:
                data = json.load(opened_file)
                data['response'] = 'No'
            with open(os.path.join(
                    utility.data_folder, 'segregation_system/responses/quality_response.json'),
                    'w',
                    encoding='utf-8') as response:
                json.dump(data, response)
        else:
            with open(os.path.join(
                    utility.data_folder, 'segregation_system/responses/quality_response.json'),
                    'r',
                    encoding='utf-8') as opened_file:
                data = json.load(opened_file)
                data['response'] = 'Yes'
            with open(os.path.join(
                    utility.data_folder, 'segregation_system/responses/quality_response.json'),
                    'w',
                    encoding='utf-8') as response:
                json.dump(data, response)

    def generate_datasets(self):
        """
        Method that manage the flow of the final phase, extracts data from the DB
        and splits them in train, validation and test sets
        """
        global TESTING_ITER
        data_extractor = DataExtractor(self.db_handler,
                                       self.current_iteration,
                                       self.config_file.session_nr_threshold)
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
        self.db_handler.update_type(self.current_iteration, self.config_file.session_nr_threshold)

        communication_controller = CommunicationController(self.db_handler,
                                                           self.config_file.development_system_url,
                                                           self)
        communication_controller.send_datasets(res.to_dict())
        print("Dataset sent, now terminate")

        # remove the generated graphs
        try:
            os.remove(os.path.join(
                    utility.data_folder, BALANCING_REPORT_PATH))
            os.remove(os.path.join(
                    utility.data_folder, QUALITY_REPORT_PATH))
        except FileNotFoundError as ex:
            print(f"Error during file removal: {ex}")

        # New testing phase
        if TESTING_PHASE:
            self.current_iteration += 1
            if self.current_iteration == TESTING_DB_RESET[TESTING_ITER]:
                self.db_handler.drop_db()
                TESTING_ITER = (TESTING_ITER + 1) % 5
                self.current_iteration = 0
            return
        sys.exit(0)

    def run(self):
        """
        Method that checks which phase we need to execute, three options are available:
        - First start:  The REST server is not started yet, so we need to start it waiting for
                        new incoming messages from Preparation system.

        - Check data balancing: The system has received enough sessions in order to generate the
                        balancing histogram, it suspended its execution waiting for the Data Analyst
                        to check if the data are correctly balanced

        -Check data quality: The Data Analyst has evaluated the data as "Balanced" and the system
                        continued its execution until the radar diagram has been generated, the
                        system suspended again waiting for the Data Analyst response
        """

        extractor = ResponseExtractor()

        while True:
            # Check if data balance graph was analyzed by human expert
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

            # Check if data quality graph was analyzed by human expert
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

            # Start the Flask server on a daemon thread
            if not self.server_started:
                communication_controller = \
                    CommunicationController(self.db_handler,
                                            self.config_file.development_system_url,
                                            self.manage_message)
                flask_thread = threading.Thread(target=communication_controller.init_rest_server,
                                                daemon=True)
                flask_thread.start()
                self.server_started = True

            # Wait for a enough sessions to generate ML sets
            self.semaphore.acquire()
            self.check_balancing()

    def manage_message(self, file_json):
        """
        Function that manage the flow after receiving a message from preparation system
        :param file_json: arrived data
        :return: None
        """
        # If our system is involved with data balancing and quality I cannot
        # accept more prepared sessions so the system discards them
        with self.lock:

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
                print(f"Error during session insert #{self.sessions_nr + 1}")
                return
            self.sessions_nr += 1
            if TESTING_PHASE:
                print(f"Arrived session #{self.sessions_nr}")
            # Check if we have enough sessions
            if self.sessions_nr != self.config_file.session_nr_threshold:
                return
            self.sessions_nr = 0
        self.semaphore.release()
