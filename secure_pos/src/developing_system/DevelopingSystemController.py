import os
import joblib

from developing_system.TrainingConfiguration import TrainingConfiguration
from developing_system.MLPTraining import MLPTraining
from developing_system.GridSearchController import GridSearchController
from developing_system.DevelopingSystemConfiguration import DevelopingSystemConfiguration
from developing_system.ClassifierArchiver import ClassifierArchiver
from developing_system.TestBestClassifier import TestBestClassifier

import utility

SYSTEM_CONFIGURATION_PATH = 'development_system/developing_system_configuration.json'
SYSTEM_CONFIGURATION_SCHEMA_PATH = 'development_system/json_schemas/developing_system_configuration_schema.json'

TRAINING_CONFIGURATION_PATH = 'development_system/training_configuration.json'
TRAINING_CONFIGURATION_SCHEMA_PATH = 'development_system/json_schemas/training_configuration_schema.json'

class DevelopingSystemController:

    def __init__(self):
        self.training_configuration = TrainingConfiguration(TRAINING_CONFIGURATION_PATH, TRAINING_CONFIGURATION_SCHEMA_PATH)
        self.developing_system_configuration = DevelopingSystemConfiguration(SYSTEM_CONFIGURATION_PATH, SYSTEM_CONFIGURATION_SCHEMA_PATH)


# creation of the controller instance
controller = DevelopingSystemController()
# first training using the average parameter read from the json file
initial_phase_classifier = MLPTraining(controller.training_configuration.is_initial_phase)
initial_phase_classifier.train_neural_network(controller.training_configuration.average_parameters)

load_path = os.path.join(utility.data_folder, 'development_system/classifiers/initial_phase_classifier.sav')
loaded_classifier = joblib.load(load_path)

classifier_for_grid_search = MLPTraining("No")
classifier_for_grid_search.set_mlp(loaded_classifier)
gs = GridSearchController(classifier_for_grid_search, controller.training_configuration)
gs.generate_grid_search_hyperparameters(controller.training_configuration.hyper_parameters)
for elem in gs.top_classifiers_object_list:
    elem.print()

classifier_archive_manager = ClassifierArchiver(controller.training_configuration.best_classifier_number)
classifier_archive_manager.delete_remaining_classifiers()

test = TestBestClassifier(controller.training_configuration)
test.test_best_classifier(classifier_archive_manager.return_path_best_classifier())
test.print()