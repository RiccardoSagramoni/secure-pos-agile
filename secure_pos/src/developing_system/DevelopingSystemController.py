from developing_system.TrainingConfiguration import TrainingConfiguration
from developing_system.MLPTraining import MLPTraining
from developing_system.GridSearchController import GridSearchController
from developing_system.DevelopingSystemConfiguration import DevelopingSystemConfiguration

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
classifier = MLPTraining(controller.training_configuration)
classifier.train_neural_network()
gs = GridSearchController(classifier, controller.training_configuration)
gs.generate_grid_search_hyperparameters()
for elem in gs.top_classifiers_object_list:
    elem.print()



