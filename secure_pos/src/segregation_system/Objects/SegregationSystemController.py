import sys
from threading import Semaphore

import pandas as pd

from sklearn.model_selection import train_test_split

from segregation_system.Objects import DataExtractor
from segregation_system.Objects.CommunicationController import CommunicationController
from segregation_system.Objects.SegregationSystemConfiguration import SegregationSystemConfiguration
from segregation_system.Objects.ResponseExtractor import ResponseExtractor
from segregation_system.Objects.Plotters import PlotterHistogram, PlotterRadarDiagram


class SegregationSystemController:
    """
    Class that manage all the logic inside the Segregation System
    """

    def __init__(self):
        self.path_db = "./database/segregationSystemDatabase.db"
        self.db_semaphore = Semaphore(1)
        self.config_file = SegregationSystemConfiguration()

    def check_balancing(self):
        """
        Method that calls the API that extracts the data
        and plot them in order to evaluate the data balancing
        :return: Null
        """
        data_extractor = DataExtractor.DataExtractor(self.path_db, self.db_semaphore)
        labels = data_extractor.count_labels()

        plotter = PlotterHistogram(labels)
        plotter.plot_data_balancing()

        # The system now needs to stop, we need to wait the Data Analyst evaluation
        sys.exit(0)

    def check_quality(self):
        """
        Method that calls the API that extracts the data
        and plot them in order to evaluate the data quality
        """
        data_extractor = DataExtractor.DataExtractor(self.path_db, self.db_semaphore)
        data = data_extractor.extract_features()

        plotter = PlotterRadarDiagram(data)
        plotter.plot_data_quality()

        # The system now needs to stop, we need to wait the Data Analyst evaluation
        sys.exit(0)

    def generate_datasets(self):
        """
        Method that manage the flow of the final phase, extracts data from the DB
        and splits them in train, validation and test sets
        """

        data_extractor = DataExtractor.DataExtractor(self.path_db, self.db_semaphore)
        data_frame_input = data_extractor.extract_features()

        data_frame_result = data_extractor.extract_labels()

        # Splitting the data into 'train' and 'other',
        # aiming for 70% train 15% validation and 15% test
        x_train, x_other, y_train, y_other = train_test_split(data_frame_input,
                                                              data_frame_result,
                                                              stratify=data_frame_result,
                                                              test_size=0.3)

        #x_validation, x_test, y_validation, y_test = train_test_split(x_other,
        #                                                              y_other,
        #                                                              stratify=y_other,
        #                                                              test_size=0.5)
        # Set data type
        x_train['type'] = 0
        #x_validation['type'] = 1
        #x_test['type'] = 2
        x_other['type'] = 1

        # Merge input with
        x_train['label'] = y_train['label']
        #x_validation['label'] = y_validation['label'] TODO fix code lines
        #x_test['label'] = y_test['label']
        x_other['label'] = y_other['label']

        #pd.concat([x_train, x_validation, x_test], ignore_index=True)
        res = pd.concat([x_train, x_other], ignore_index=True)

        res.to_json('./to_fab.json')

        # Mark the records as USED TODO remove comment below
        # database.update("UPDATE ArrivedSessions SET type = 0 WHERE type = -1")

        cc = CommunicationController(self.db_semaphore, self.path_db, self)
        cc.send_datasets(res, self.config_file.development_system_url)
        print("Dataset sent, now terminate")

        # reset the mode to accept more data from now on
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
        extractor = ResponseExtractor()

        result_balancing = extractor.extract_json_response_balancing()
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

        result_quality = extractor.extract_json_response_quality()

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

        communication_handler = CommunicationController(self.db_semaphore,
                                                        self.path_db,
                                                        self.config_file.development_system_url,
                                                        self)
        #communication_handler.init_rest_server()
        communication_handler.handle_message()
