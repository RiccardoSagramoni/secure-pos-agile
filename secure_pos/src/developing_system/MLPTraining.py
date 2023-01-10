import os

from sklearn.neural_network import MLPClassifier
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay, accuracy_score
from pandas import read_csv
from numpy import ravel
import matplotlib.pyplot as plt
import joblib

from developing_system.TrainingConfiguration import TrainingConfiguration
import utility

class MLPTraining:

    def __init__(self, is_initial_phase):

        # data from the json training_configuration file
        self.is_initial_phase = is_initial_phase

        # dataset for the training and validation
        self.training_data = read_csv('prova/trainingData.csv')
        self.training_labels = read_csv('prova/trainingLabels.csv')
        self.validation_data = read_csv('prova/testingData.csv')
        self.validation_labels = read_csv('prova/testingLabels.csv')

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

        if self.is_initial_phase in ["Yes", "yes"]:

            # plot of the loss function in function of the number of generations
            plt.plot(self.mlp.loss_curve_)
            plt.xlabel("Number of Generations")
            plt.ylabel("Loss Function")
            plt.title("LOSS FUNCTION PLOT")
            plt.savefig("plots/loss_function_plot.png")
            plt.show()

            save_path = os.path.join(utility.data_folder, 'development_system/classifiers/initial_phase_classifier.sav')
            joblib.dump(self.mlp, save_path)
