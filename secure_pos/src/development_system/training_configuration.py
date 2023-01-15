import json
import logging
import os

import utility
from utility.json_validation import validate_json_data_file


class TrainingConfiguration:

    def __init__(self, json_training_configuration_path: str, json_schema_path: str):
        # Open configuration file
        with open(os.path.join(utility.data_folder, json_training_configuration_path), "r",
                  encoding="UTF-8") as file:
            # Load JSON configuration
            json_training_conf = json.load(file)
            # Validate configuration
            if not validate_json_data_file(json_training_conf, json_schema_path):
                logging.error("Impossible to load the training "
                              "configuration: JSON file is not valid")
                raise ValueError("Training configuration failed")

            # Add JSON attributes to current object
            self.hyper_parameters = json_training_conf['hyper_parameters']
            self.average_parameters = json_training_conf['average_params']
            self.test_tolerance = json_training_conf['test_tolerance']
            self.number_of_top_classifiers = int(json_training_conf['number_of_top_classifiers'])
            self.validation_tolerance = json_training_conf['validation_tolerance']
            self.is_initial_phase_over = json_training_conf['is_initial_phase_over']
            self.is_grid_search_over = json_training_conf['is_grid_search_over']
            self.best_classifier_number = int(json_training_conf['best_classifier_number'])
            self.test_best_classifier_passed = json_training_conf['test_best_classifier_passed']
