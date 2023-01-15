import os

from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score
from numpy import ravel
import matplotlib.pyplot as plt
import joblib

from development_system.initial_phase_training_report_generator import InitialPhaseTrainingReportGenerator
from development_system.machine_learning_sets_archiver import MachineLearningSetsArchiver
import utility

TRAINING_SETS = 0
VALIDATION_SETS = 1


class MLPTraining:

    def __init__(self, is_initial_phase, ml_sets_archive_handler: MachineLearningSetsArchiver):

        # data from the json training_configuration file
        self.is_initial_phase_over = is_initial_phase

        [training_data, training_labels] = ml_sets_archive_handler.get_ml_sets(TRAINING_SETS)
        [validation_data, validation_labels] = ml_sets_archive_handler.get_ml_sets(VALIDATION_SETS)

        # dataset for the training and validation
        self.training_data = training_data
        self.training_labels = training_labels
        self.validation_data = validation_data
        self.validation_labels = validation_labels

        # results of the single training
        self.mlp = None
        self.validation_error = None
        self.training_error = None

    def set_mlp(self, setted_mlp):
        self.mlp = setted_mlp

    def train_neural_network(self, setted_hyper_parameters):

        # declaration of the mlp with the hyperparameters
        self.mlp = MLPClassifier(**setted_hyper_parameters)

        # training of the mlp using the training set
        self.mlp.fit(self.training_data, ravel(self.training_labels))
        self.training_error = 1 - (self.mlp.score(self.training_data, ravel(self.training_labels)))

        # prediction of the risk labels using the validation set
        attack_risk_label_prediction = self.mlp.predict(self.validation_data)
        # measure the accurancy using the validation set
        self.validation_error = 1 - (accuracy_score(ravel(self.validation_labels), attack_risk_label_prediction))

        if self.is_initial_phase_over in ['No', 'no', 'NO']:

            # plot of the loss function in function of the number of generations
            plt.plot(self.mlp.loss_curve_)
            plt.xlabel("Number of Generations")
            plt.ylabel("Loss Function")
            plt.title("LOSS FUNCTION PLOT")
            plt.savefig(os.path.join(utility.data_folder,
                                     'development_system/reports/initial_phase/loss_function_plot.png'))
            # plt.show()
            plt.clf()

            InitialPhaseTrainingReportGenerator.generate_report(self.training_error,
                                                                self.validation_error,
                                                                setted_hyper_parameters)

            save_path = os.path.join(utility.data_folder, 'development_system/classifiers/initial_phase_classifier.sav')
            joblib.dump(self.mlp, save_path)
