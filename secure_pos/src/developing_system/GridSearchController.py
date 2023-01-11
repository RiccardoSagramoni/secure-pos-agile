import os

import joblib
from sklearn.model_selection import ParameterGrid

import utility
from developing_system.TrainingConfiguration import TrainingConfiguration
from developing_system.TopClassifier import TopClassifier
from developing_system.TopClassifiersReportGenerator import TopClassifierReportGenerator


class GridSearchController:

    def __init__(self, mlp_classifier, training_conf:TrainingConfiguration):

        # data from the json training_configuration file
        self.validation_tolerance = training_conf.validation_tolerance
        self.number_of_top_classifiers = training_conf.number_of_top_classifiers

        # necessary field for the gridsearch algorithm
        self.mlp_training_for_grid_search = mlp_classifier
        self.validation_errors_of_top_classifiers = dict.fromkeys([1, 2, 3, 4, 5])
        self.top_classifiers_object_list = []


    def save_classifier_among_top_classifier(self, id_classifier, possible_hyperparameters_combination):
        top_classifier = TopClassifier(id_classifier, self.mlp_training_for_grid_search, possible_hyperparameters_combination)
        if len(self.top_classifiers_object_list) == self.number_of_top_classifiers:
            self.top_classifiers_object_list[id_classifier - 1] = top_classifier
        else:
            self.top_classifiers_object_list.insert(id_classifier - 1, top_classifier)

        filename_classifier = "classifier_number_" + str(id_classifier) + ".sav"
        save_path = os.path.join(utility.data_folder, 'development_system/classifiers/'+ filename_classifier)
        joblib.dump(self.mlp_training_for_grid_search.mlp, save_path)



    def check_validation_error_classifier(self, index, possible_hyperparameters_combination):

        if index <= self.number_of_top_classifiers:
            self.validation_errors_of_top_classifiers.update({index: self.mlp_training_for_grid_search.validation_error})
            self.save_classifier_among_top_classifier(index, possible_hyperparameters_combination)

        else:
            key_value_with_max_validation_error = max(self.validation_errors_of_top_classifiers, key=self.validation_errors_of_top_classifiers.get)
            if self.mlp_training_for_grid_search.validation_error not in self.validation_errors_of_top_classifiers.values() and self.mlp_training_for_grid_search.validation_error < self.validation_errors_of_top_classifiers.get(key_value_with_max_validation_error):
                self.validation_errors_of_top_classifiers.update({key_value_with_max_validation_error: self.mlp_training_for_grid_search.validation_error})
                self.save_classifier_among_top_classifier(key_value_with_max_validation_error, possible_hyperparameters_combination)


    def generate_grid_search_hyperparameters(self, setted_hyper_parameters):

        grid_search = list(ParameterGrid(setted_hyper_parameters))
        index = 1
        for possible_hyperparameters_combination in grid_search:
            print(f"Combinazione {index}")
            self.mlp_training_for_grid_search.train_neural_network(possible_hyperparameters_combination)
            self.check_validation_error_classifier(index, possible_hyperparameters_combination)
            index = index + 1

        print(self.validation_errors_of_top_classifiers)

        TopClassifierReportGenerator().generate_report(self)


