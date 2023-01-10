from sklearn.model_selection import ParameterGrid
from developing_system.TrainingConfiguration import TrainingConfiguration
from developing_system.TopClassifier import TopClassifier


class GridSearchController:

    def __init__(self, mlp_classifier, training_conf:TrainingConfiguration):

        # data from the json training_configuration file
        self.validation_tolerance = training_conf.validation_tolerance
        self.number_of_top_classifiers = training_conf.number_of_top_classifiers
        self.hyper_parameters = training_conf.hyper_parameters

        # necessary field for the gridsearch algorithm
        self.classifier = mlp_classifier
        self.validation_errors_of_top_classifiers = dict.fromkeys([1, 2, 3, 4, 5])
        self.top_classifiers_object_list = []

    def save_classifier_among_top_classifier(self, id_classifier):
        top_classifier = TopClassifier(id_classifier, self.classifier)
        if len(self.top_classifiers_object_list) == self.number_of_top_classifiers:
            self.top_classifiers_object_list[id_classifier - 1] = top_classifier
        else:
            self.top_classifiers_object_list.insert(id_classifier - 1, top_classifier)


    def check_validation_error_classifier(self, index):

        if index <= self.number_of_top_classifiers:
            self.validation_errors_of_top_classifiers.update({index: self.classifier.validation_error})
            self.save_classifier_among_top_classifier(index)

        else:
            key_value_with_max_validation_error = max(self.validation_errors_of_top_classifiers, key=self.validation_errors_of_top_classifiers.get)
            if self.classifier.validation_error not in self.validation_errors_of_top_classifiers.values() and self.classifier.validation_error < self.validation_errors_of_top_classifiers.get(key_value_with_max_validation_error):
                self.validation_errors_of_top_classifiers.update({key_value_with_max_validation_error: self.classifier.validation_error})
                self.save_classifier_among_top_classifier(key_value_with_max_validation_error)


    def generate_grid_search_hyperparameters(self):

        grid_search = list(ParameterGrid(self.hyper_parameters))
        index = 1
        for possible_hyperparameters_combination in grid_search:
            print(f"Combinazione {index}")
            self.classifier.set_hyperparameters(False, **possible_hyperparameters_combination)
            self.classifier.train_neural_network()
            self.check_validation_error_classifier(index)
            index = index + 1

        print(self.validation_errors_of_top_classifiers)


