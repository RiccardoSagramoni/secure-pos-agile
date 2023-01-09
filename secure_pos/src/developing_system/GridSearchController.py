from sklearn.model_selection import ParameterGrid
from developing_system.MLPTraining import MLPTraining


class GridSearchController:

    def __init__(self, classifier):

        self.tolerance_threshold = None
        self.classifier = classifier

    def set_tolerance_threshold(self, selected_tolerance):
        self.tolerance_threshold = selected_tolerance

    def generate_grid_search_hyperparameters(self):

        hyper_parameters = {'first_hidden_layer_size': [80, 100, 120],
                            'activation': ["relu", "tanh", "logistic"],
                            'solver': ["adam", "sgd", "lbfgs"],
                            'learning_rate': ['constant', 'invscaling', 'constant']}

        grid_search = list(ParameterGrid(hyper_parameters))
        index = 0
        for possible_hyperparameters_combination in grid_search:
            print(f"Round {index}: hyperparameters:{possible_hyperparameters_combination}")
            self.classifier.set_hyperparameters(False,
                                                first_hidden_layer_size = possible_hyperparameters_combination['first_hidden_layer_size'],
                                                activation = possible_hyperparameters_combination['activation'],
                                                solver = possible_hyperparameters_combination['solver'],
                                                learning_rate_mode = possible_hyperparameters_combination['learning_rate'])
            index = index + 1
            self.classifier.train_neural_network()


classifier = MLPTraining()
gs = GridSearchController(classifier)
gs.generate_grid_search_hyperparameters()
