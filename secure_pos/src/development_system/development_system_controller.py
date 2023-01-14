import logging
import os
import sys
import threading
import time
import pandas as pd
import joblib
import json
import random
from os import path

from development_system.training_configuration import TrainingConfiguration
from development_system.mlp_training import MLPTraining
from development_system.grid_search_controller import GridSearchController
from development_system.development_system_configuration import DevelopmentSystemConfiguration
from development_system.development_system_archiver import DevelopmentSystemArchiver
from development_system.test_best_classifier import TestBestClassifier
from development_system.development_system_communication_controller import DevelopmentSystemCommunicationController
from development_system.machine_learning_sets_archiver import MachineLearningSetsArchiver

import utility

SYSTEM_CONFIGURATION_PATH = 'development_system/configuration_files/development_system_configuration.json'
SYSTEM_CONFIGURATION_SCHEMA_PATH = 'development_system/json_schemas/development_system_configuration_schema.json'
TRAINING_CONFIGURATION_PATH = 'development_system/configuration_files/training_configuration.json'
TRAINING_CONFIGURATION_SCHEMA_PATH = 'development_system/json_schemas/training_configuration_schema.json'

ML_SETS_ARCHIVE_PATH = 'development_system/ml_sets_archive/ml_sets_archive.db'
ML_SETS_JSON_FILE_PATH = 'development_system/received_files/ml_set_for_training_classifier.json'

INITIAL_PHASE = 1
SELECT_BEST_CLASSIFIER_PHASE = 2
TEST_BEST_CLASSIFIER_PASSED_PHASE = 3

TESTING_MODE = False

class DevelopmentSystemController:

    semaphore = threading.Semaphore(0)
    status = None
    final_phase_over = False

    def __init__(self):
        self.training_configuration = TrainingConfiguration(TRAINING_CONFIGURATION_PATH, TRAINING_CONFIGURATION_SCHEMA_PATH)
        self.developing_system_configuration = DevelopmentSystemConfiguration(SYSTEM_CONFIGURATION_PATH, SYSTEM_CONFIGURATION_SCHEMA_PATH)
        self.communication_controller = DevelopmentSystemCommunicationController(self.developing_system_configuration, self.save_ml_sets_in_the_archive, self.semaphore.release)
        self.ml_sets_archive_handler = MachineLearningSetsArchiver(os.path.join(utility.data_folder, ML_SETS_ARCHIVE_PATH))

    def execution_of_the_initial_phase_training(self):

        initial_phase_classifier = MLPTraining(self.training_configuration.is_initial_phase_over, self.ml_sets_archive_handler)
        initial_phase_classifier.train_neural_network(self.training_configuration.average_parameters)
        print("Initial Phase Training is finished")
        if TESTING_MODE:
            get_random_response_for_execution_control(1)

    def execution_of_the_grid_search_algorithm(self):

        loaded_classifier = joblib.load(os.path.join(utility.data_folder, 'development_system/classifiers/initial_phase_classifier.sav'))
        classifier_for_grid_search = MLPTraining(self.training_configuration.is_initial_phase_over, self.ml_sets_archive_handler)
        classifier_for_grid_search.set_mlp(loaded_classifier)
        grid_search_controller = GridSearchController(classifier_for_grid_search, self.training_configuration)
        grid_search_controller.generate_grid_search_hyperparameters(self.training_configuration.hyper_parameters)
        print("Grid Search Algorithm is finished")

        with open(os.path.join(utility.data_folder,TRAINING_CONFIGURATION_PATH), 'r') as read_file:
            json_data = json.load(read_file)
            json_data['is_grid_search_over'] = "Yes"

        with open(os.path.join(utility.data_folder,TRAINING_CONFIGURATION_PATH), 'w') as write_file:
            json.dump(json_data, write_file, indent=2)

        if TESTING_MODE:
            get_random_response_for_execution_control(2)

    def analysis_of_the_best_classifier(self):

        DevelopmentSystemArchiver.delete_remaining_classifiers(self.training_configuration.best_classifier_number)
        training_error_best_classifier = None

        with open(os.path.join(utility.data_folder, 'development_system/reports/top_classifiers/report_top_classifiers.json'), 'r') as report:
            json_data = json.load(report)
            for i in json_data['top_classifiers']:
                if i['classifier_id'] == self.training_configuration.best_classifier_number:
                    training_error_best_classifier = i['training_error']

        test = TestBestClassifier(self.training_configuration, training_error_best_classifier, self.ml_sets_archive_handler)
        test.test_best_classifier(DevelopmentSystemArchiver.return_path_best_classifier(self.training_configuration.best_classifier_number))
        print("the best classifier has been analyzed")
        if TESTING_MODE:
            get_random_response_for_execution_control(3)

    def reset_of_the_system(self):

        with open(os.path.join(utility.data_folder,TRAINING_CONFIGURATION_PATH), 'r') as read_file:
            json_data = json.load(read_file)
            json_data['is_initial_phase_over'] = "No"
            json_data['is_grid_search_over'] = "No"
            json_data['test_best_classifier_passed'] = "None"
            json_data['best_classifier_number'] = 0

        with open(os.path.join(utility.data_folder,TRAINING_CONFIGURATION_PATH), 'w') as write_file:
            json.dump(json_data, write_file, indent=2)

        DevelopmentSystemArchiver.delete_all_file_in_the_directory(os.path.join(utility.data_folder,'development_system'))

        print("the system has been reset")

    def run(self):

        with open(os.path.join(utility.data_folder, 'development_system/development_status.json'), 'r') as read_status:
            json_data = json.load(read_status)
            self.status = json_data["status"]

        # creation and start of the server flask
        flask_thread = threading.Thread(target=self.communication_controller.start_developing_rest_server, daemon=True)
        flask_thread.start()

        # initialize del counter
        # start the execution control of the development system
        while True:

            if self.status == "Running":
                self.semaphore.acquire()
                time.sleep(1)
                ret = self.ml_sets_archive_handler.insert_ml_sets()
                if not ret:
                    logging.error("Failed to insert the data received in the archive")
                    sys.exit(0)
                else:
                    print("a new ml sets table is created")
            else:
                self.status = "Running"

            # incremnet counter
            self.execution_control_of_the_development_system()

    def execution_control_exit(self):

        if TESTING_MODE:
            self.execution_control_of_the_development_system()
        else:
            if self.final_phase_over:

                json_data = {
                    "status": "Running"
                }
                self.final_phase_over = False

            else:

                json_data = {
                    "status": "Waiting"
                }

            with open(os.path.join(utility.data_folder, 'development_system/development_status.json'), 'w') as write_status:
                write_status.write(json.dumps(json_data, indent=2))

            sys.exit(0)

    def execution_control_of_the_development_system(self):

        if TESTING_MODE:
            self.training_configuration = TrainingConfiguration(TRAINING_CONFIGURATION_PATH,
                                                            TRAINING_CONFIGURATION_SCHEMA_PATH)

        yes_response = ["Yes", "YES", "yes", "yES"]
        no_response = ["No", "NO", "no", "nO"]

        if self.training_configuration.test_best_classifier_passed != "None":
            # the test of the best classifier is executed
            if self.training_configuration.test_best_classifier_passed in no_response or self.training_configuration.test_best_classifier_passed in yes_response:
                # the ML Engineer has correctly inserted the response of the test
                self.ml_sets_archive_handler.drop_ml_sets_table()
                if self.training_configuration.test_best_classifier_passed in yes_response:
                    # the test is passed and the classifier will be sent to the execution system
                    self.communication_controller.send_classifier_to_execution_system(DevelopmentSystemArchiver.return_path_best_classifier(self.training_configuration.best_classifier_number))
                self.reset_of_the_system()
                if TESTING_MODE:
                    return
                else:
                    self.final_phase_over = True
                    self.execution_control_exit()
            else:
                print("Unknown value for 'test_best_classifier_passed' param, in the training configuration file: \
                        please insert 'yes' or 'no'")
                self.execution_control_exit()
        else:
            # the test of the best classifier is not executed yet, so the test_best_classifier_passed param is 'None'
            if self.training_configuration.best_classifier_number != 0:
                # the grid search was executed and the top classifier were found
                # and the ML Engineer has chosen the best classifier
                if 1 <= self.training_configuration.best_classifier_number <= self.training_configuration.number_of_top_classifiers:
                    # the ML Engineer has correctly inserted the best classifier
                    self.analysis_of_the_best_classifier()
                    self.execution_control_exit()
                else:
                    print("Unknown value for 'best_classifier_number' param, in the training configuration file: \
                            please insert a number between 1 and number_of_top_classifiers")
                    self.execution_control_exit()
            else:
                if self.training_configuration.is_grid_search_over in yes_response:
                    # the grid search was executed and the top classifier were found
                    # but the ML Engineer could not choose the best one because no one met the tolerance requirement
                    self.reset_of_the_system()
                    self.execution_control_exit()
                elif self.training_configuration.is_grid_search_over in no_response:
                    # the grid search was not executed
                    if self.training_configuration.is_initial_phase_over in yes_response:
                        # the initial phase training was executed and the grid search will be executed
                        self.execution_of_the_grid_search_algorithm()
                        self.execution_control_exit()
                    elif self.training_configuration.is_initial_phase_over in no_response:
                        # the initial phase training has not been executed or must be re-executed
                        self.execution_of_the_initial_phase_training()
                        self.execution_control_exit()
                    else:
                        print("Unknown value for 'is_initial_phase_over' param, in the training configuration file: \
                                please insert 'yes' or 'no'")
                        self.execution_control_exit()
                else:
                    print("Unknown value for 'is_grid_search_over' param, in the training configuration file: please insert 'yes' or 'no'")
                    self.execution_control_exit()

    def save_ml_sets_in_the_archive(self, json_data):

        file_json_path = os.path.join(utility.data_folder, ML_SETS_JSON_FILE_PATH)

        with open(file_json_path, 'w') as file_to_save:
            json.dump(json_data, file_to_save, indent=2)

        self.ml_sets_archive_handler.create_json_received_table()

        y = json.dumps(json_data)
        # data = {'sets': [json_data]}
        received_json_data_frame = pd.DataFrame([y], columns=['sets'])
        #
        print(received_json_data_frame)

        ret = self.ml_sets_archive_handler.insert_json_received(received_json_data_frame)
        if not ret:
            logging.error("Failed to insert the data received in the archive")
            sys.exit(0)
        else:
            print("the ml sets received by the segregation system were saved")

def get_random_response_for_execution_control(step):

    with open(os.path.join(utility.data_folder, TRAINING_CONFIGURATION_PATH), 'r') as read_file:

        json_data = json.load(read_file)

        random_number = random.randint(0, 10)
        if step == 1:
            if random_number <= 7:
                json_data['is_initial_phase_over'] = "Yes"
            else:
                json_data['is_initial_phase_over'] = "No"
        elif step == 2:
            if random_number <= 8:
                json_data['best_classifier_number'] = 0
            else:
                json_data['best_classifier_number'] = random.randint(1, 5)
        else:
            if random_number <= 9:
                json_data['test_best_classifier_passed'] = "Yes"
            else:
                json_data['test_best_classifier_passed'] = "No"

    with open(os.path.join(utility.data_folder, TRAINING_CONFIGURATION_PATH), 'w') as write_file:
        json.dump(json_data, write_file, indent=2)
