import logging
import os
import sys
import threading
import time
import pandas as pd
import joblib
import json
from os import path

from development_system.TrainingConfiguration import TrainingConfiguration
from development_system.MLPTraining import MLPTraining
from development_system.GridSearchController import GridSearchController
from development_system.DevelopmentSystemConfiguration import DevelopmentSystemConfiguration
from development_system.DevelopmentSystemArchiver import DevelopmentSystemArchiver
from development_system.TestBestClassifier import TestBestClassifier
from development_system.DevelopmentSystemCommunicationController import DevelopmentSystemCommunicationController
from development_system.MachineLearningSetsArchiver import MachineLearningSetsArchiver

import utility

SYSTEM_CONFIGURATION_PATH = 'development_system/configuration_files/development_system_configuration.json'
SYSTEM_CONFIGURATION_SCHEMA_PATH = 'development_system/json_schemas/development_system_configuration_schema.json'
TRAINING_CONFIGURATION_PATH = 'development_system/configuration_files/training_configuration.json'
TRAINING_CONFIGURATION_SCHEMA_PATH = 'development_system/json_schemas/training_configuration_schema.json'

ML_SETS_ARCHIVE_PATH = 'development_system/ml_sets_archive/ml_sets_archive.db'
ML_SETS_JSON_FILE_PATH = 'development_system/received_files/ml_set_for_training_classifier.json'

class DevelopmentSystemController:

    semaphore = threading.Semaphore(0)

    def __init__(self):
        self.training_configuration = TrainingConfiguration(TRAINING_CONFIGURATION_PATH, TRAINING_CONFIGURATION_SCHEMA_PATH)
        self.developing_system_configuration = DevelopmentSystemConfiguration(SYSTEM_CONFIGURATION_PATH, SYSTEM_CONFIGURATION_SCHEMA_PATH)
        self.communication_controller = DevelopmentSystemCommunicationController(self.developing_system_configuration, self.save_ml_sets_in_the_archive, self.semaphore.release)
        self.ml_sets_archive_handler = MachineLearningSetsArchiver(os.path.join(utility.data_folder, ML_SETS_ARCHIVE_PATH))


    def execution_of_the_initial_phase_training(self):

        initial_phase_classifier = MLPTraining(self.training_configuration.is_initial_phase_over, self.ml_sets_archive_handler)
        initial_phase_classifier.train_neural_network(self.training_configuration.average_parameters)


    def execution_of_the_grid_search_algorithm(self):

        loaded_classifier = joblib.load(os.path.join(utility.data_folder, 'development_system/classifiers/initial_phase_classifier.sav'))
        classifier_for_grid_search = MLPTraining(self.training_configuration.is_initial_phase_over, self.ml_sets_archive_handler)
        classifier_for_grid_search.set_mlp(loaded_classifier)
        grid_search_controller = GridSearchController(classifier_for_grid_search, self.training_configuration)
        grid_search_controller.generate_grid_search_hyperparameters(self.training_configuration.hyper_parameters)
        for elem in grid_search_controller.top_classifiers_object_list:
            elem.print()

        with open(os.path.join(utility.data_folder,TRAINING_CONFIGURATION_PATH), 'r') as read_file:
            json_data = json.load(read_file)
            json_data['is_grid_search_over'] = "Yes"

        with open(os.path.join(utility.data_folder,TRAINING_CONFIGURATION_PATH), 'w') as write_file:
            json.dump(json_data, write_file, indent=2)


    def reset_of_the_system(self):

        with open(os.path.join(utility.data_folder,TRAINING_CONFIGURATION_PATH), 'r') as read_file:
            json_data = json.load(read_file)
            json_data['is_initial_phase_over'] = "No"
            json_data['is_grid_search_over'] = "No"
            json_data['test_best_classifier_passed'] = "None"
            json_data['best_classifier_number'] = 0

        with open(os.path.join(utility.data_folder,TRAINING_CONFIGURATION_PATH), 'w') as write_file:
            json.dump(json_data, write_file, indent=2)

        classifier_archive_manager = DevelopmentSystemArchiver(self.training_configuration.best_classifier_number)
        classifier_archive_manager.delete_all_file_in_the_directory(os.path.join(utility.data_folder,'development_system'))


    def run(self):

        if path.exists(os.path.join(utility.data_folder,ML_SETS_ARCHIVE_PATH)):

            self.execution_of_the_development_system()
            sys.exit(0)

        else:

            flask_thread = threading.Thread(target=self.communication_controller.start_developing_rest_server, daemon=True)
            flask_thread.start()
            self.semaphore.acquire()

            time.sleep(1)
            self.execution_of_the_development_system()
            sys.exit(0)


    def analysis_of_the_best_classifier(self):

        classifier_archive_manager = DevelopmentSystemArchiver(self.training_configuration.best_classifier_number)
        classifier_archive_manager.delete_remaining_classifiers()
        training_error_best_classifier = None

        with open(os.path.join(utility.data_folder, 'development_system/reports/top_classifiers/report_top_classifiers.json'), 'r') as report:
            json_data = json.load(report)
            for i in json_data['top_classifiers']:
                if i['classifier_id'] == self.training_configuration.best_classifier_number:
                    training_error_best_classifier = i['training_error']

        test = TestBestClassifier(self.training_configuration, training_error_best_classifier, self.ml_sets_archive_handler)
        test.test_best_classifier(classifier_archive_manager.return_path_best_classifier())
        test.print()


    def execution_of_the_development_system(self):

        yes_response = ["Yes", "YES", "yes", "yES"]
        no_response = ["No", "NO", "no", "nO"]

        if self.training_configuration.test_best_classifier_passed != "None":
            # the test of the best classifier is executed
            if self.training_configuration.test_best_classifier_passed in no_response or self.training_configuration.test_best_classifier_passed in yes_response:
                # the ML Engineer has correctly inserted the response of the test
                self.ml_sets_archive_handler.drop_ml_sets_db()
                if self.training_configuration.test_best_classifier_passed in yes_response:
                    # the test is passed and the classifier will be sent to the execution system
                    classifier_archive_manager = DevelopmentSystemArchiver(self.training_configuration.best_classifier_number)
                    self.communication_controller.send_classifier_to_execution_system(classifier_archive_manager.return_path_best_classifier())
                self.reset_of_the_system()
                sys.exit(0)
            else:
                print("Unknown value for 'test_best_classifier_passed' param, in the training configuration file: \
                        please insert 'yes' or 'no'")
                sys.exit(0)
        else:
            # the test of the best classifier is not executed yet, so the test_best_classifier_passed param is 'None'
            if self.training_configuration.best_classifier_number != 0:
                # the grid search was executed and the top classifier were found
                # and the ML Engineer has chosen the best classifier
                if 1 <= self.training_configuration.best_classifier_number <= self.training_configuration.number_of_top_classifiers:
                    # the ML Engineer has correctly inserted the best classifier
                    self.analysis_of_the_best_classifier()
                    sys.exit(0)
                else:
                    print("Unknown value for 'best_classifier_number' param, in the training configuration file: \
                            please insert a number between 1 and number_of_top_classifiers")
                    sys.exit(0)
            else:
                if self.training_configuration.is_grid_search_over in yes_response:
                    # the grid search was executed and the top classifier were found
                    # but the ML Engineer could not choose the best one because no one met the tolerance requirement
                    self.reset_of_the_system()
                    sys.exit(0)
                elif self.training_configuration.is_grid_search_over in no_response:
                    # the grid search was not executed
                    if self.training_configuration.is_initial_phase_over in yes_response:
                        # the initial phase training was executed and the grid search will be executed
                        self.execution_of_the_grid_search_algorithm()
                        sys.exit(0)
                    elif self.training_configuration.is_initial_phase_over in no_response:
                        # the initial phase training has not been executed or must be re-executed
                        self.execution_of_the_initial_phase_training()
                        sys.exit(0)
                    else:
                        print("Unknown value for 'is_initial_phase_over' param, in the training configuration file: \
                                please insert 'yes' or 'no'")
                        sys.exit(0)
                else:
                    print("Unknown value for 'is_grid_search_over' param, in the training configuration file: please insert 'yes' or 'no'")
                    sys.exit(0)


    def save_ml_sets_in_the_archive(self, json_data):

        file_json_path = os.path.join(utility.data_folder, ML_SETS_JSON_FILE_PATH)

        with open(file_json_path, 'w') as file_to_save:
            json.dump(json_data, file_to_save, indent=2)

        self.ml_sets_archive_handler.create_ml_sets_table()

        data_frame = pd.DataFrame(json_data,
                                  columns= ['id','time_mean', 'time_median', 'time_std',
                                           'time_kurtosis', 'time_skewness', 'amount_mean',
                                           'amount_median', 'amount_std', 'amount_kurtosis',
                                           'amount_skewness', 'type', 'label'])

        ret = self.ml_sets_archive_handler.insert_ml_sets(data_frame)
        if not ret:
            logging.error("Failed to insert the data received in the archive")
            sys.exit(0)
