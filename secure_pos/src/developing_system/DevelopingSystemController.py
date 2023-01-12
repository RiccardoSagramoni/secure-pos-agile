import logging
import os
import sys
import threading
import time
import pandas as pd
import joblib
import json
from os import path

from developing_system.TrainingConfiguration import TrainingConfiguration
from developing_system.MLPTraining import MLPTraining
from developing_system.GridSearchController import GridSearchController
from developing_system.DevelopingSystemConfiguration import DevelopingSystemConfiguration
from developing_system.ClassifierArchiver import ClassifierArchiver
from developing_system.TestBestClassifier import TestBestClassifier
from developing_system.TestBestClassifierReportGenerator import TestBestCLassifierReportGenerator
from developing_system.CommunicationController import CommunicationController
from developing_system.MachineLearningSetsArchiver import MachineLearningSetsArchiver

import utility

SYSTEM_CONFIGURATION_PATH = 'development_system/configuration_files/developing_system_configuration.json'
SYSTEM_CONFIGURATION_SCHEMA_PATH = 'development_system/json_schemas/developing_system_configuration_schema.json'

TRAINING_CONFIGURATION_PATH = 'development_system/configuration_files/training_configuration.json'
TRAINING_CONFIGURATION_SCHEMA_PATH = 'development_system/json_schemas/training_configuration_schema.json'

ML_SETS_ARCHIVE_PATH = 'development_system/ml_sets_archive/ml_sets_archive.db'
ML_SETS_JSON_FILE_PATH = 'development_system/received_files/ml_set_for_training_classifier.json'


class DevelopingSystemController:

    semaphore = threading.Semaphore(0)

    def __init__(self):
        self.training_configuration = TrainingConfiguration(TRAINING_CONFIGURATION_PATH, TRAINING_CONFIGURATION_SCHEMA_PATH)
        self.developing_system_configuration = DevelopingSystemConfiguration(SYSTEM_CONFIGURATION_PATH, SYSTEM_CONFIGURATION_SCHEMA_PATH)
        self.communication_controller = CommunicationController(self.developing_system_configuration, self.save_ml_sets_in_the_archive, self.semaphore.release)
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

    def reset_of_the_system(self):
        classifier_archive_manager = ClassifierArchiver(self.training_configuration.best_classifier_number)
        classifier_archive_manager.delete_remaining_classifiers()
        with open(os.path.join(utility.data_folder,TRAINING_CONFIGURATION_PATH), 'r') as read_file:
            json_data = json.load(read_file)
            json_data['is_initial_phase_over'] = "No"
            json_data['is_grid_search_over'] = "No"

        with open(os.path.join(utility.data_folder,TRAINING_CONFIGURATION_PATH), 'w') as write_file:
            json.dump(json_data, write_file, indent=2)

    def run(self):

        if path.exists(os.path.join(utility.data_folder,ML_SETS_ARCHIVE_PATH)):

            self.identify_the_top_mlp_classifiers()
            sys.exit(0)

        else:

            flask_thread = threading.Thread(target=self.communication_controller.start_developing_rest_server, daemon=True)
            flask_thread.start()
            self.semaphore.acquire()

            time.sleep(1)
            self.identify_the_top_mlp_classifiers()
            sys.exit(0)


    def analysis_of_the_best_classifier(self):

        classifier_archive_manager = ClassifierArchiver(self.training_configuration.best_classifier_number)
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



    def identify_the_top_mlp_classifiers(self):

        if self.training_configuration.best_classifier_number == 0:
            if self.training_configuration.is_grid_search_over in ['No', 'no', 'NO']:
                if self.training_configuration.is_initial_phase_over in ['No', 'no', 'NO']:
                    self.execution_of_the_initial_phase_training()
                    sys.exit(0)
                elif self.training_configuration.is_initial_phase_over in ['Yes', 'yes', 'YES']:
                    self.execution_of_the_grid_search_algorithm()
                    sys.exit(0)
                else:
                    print("Unknown value for 'is_initial_phase_over' param, in the training configuration file: please insert 'yes' or 'no'")
                    sys.exit(0)

            elif self.training_configuration.is_grid_search_over in ['Yes', 'yes', 'YES']:
                self.reset_of_the_system()
                sys.exit(0)

            else:

                print("Unknown value for 'is_grid_search_over' param, in the training configuration file: please insert 'yes' or 'no'")
                sys.exit(0)

        else:

            if self.training_configuration.test_best_classifier_passed in ['None', 'none', 'NONE']:
                self.analysis_of_the_best_classifier()
                sys.exit(0)

            else:
                if self.training_configuration.test_best_classifier_passed in ['Yes', 'yes', 'YES']:

                    classifier_archive_manager = ClassifierArchiver(self.training_configuration.best_classifier_number)
                    self.communication_controller.send_classifier_to_execution_system(classifier_archive_manager.return_path_best_classifier())
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





