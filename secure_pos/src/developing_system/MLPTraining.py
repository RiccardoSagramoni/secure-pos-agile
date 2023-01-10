from sklearn.neural_network import MLPClassifier
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay, accuracy_score
from pandas import read_csv
from numpy import ravel
import matplotlib.pyplot as plt

from developing_system.TrainingConfiguration import TrainingConfiguration

class MLPTraining:

    def __init__(self, training_conf: TrainingConfiguration):

        # data from the json training_configuration file
        self.is_initial_phase = training_conf.is_initial_phase
        self.generation_number = training_conf.generation_number
        self.hyper_parameters = training_conf.average_parameters

        # dataset for the training and validation
        self.training_data = read_csv('prova/trainingData.csv')
        self.training_labels = read_csv('prova/trainingLabels.csv')
        self.validation_data = read_csv('prova/testingData.csv')
        self.validation_labels = read_csv('prova/testingLabels.csv')

        # results of the single training
        self.mlp = None
        self.validation_error = None
        self.training_error = None


    def set_hyperparameters(self, is_initial_phase, **setted_hyper_parameters):

        self.is_initial_phase = is_initial_phase
        self.hyper_parameters = setted_hyper_parameters


    def train_neural_network(self):

        # declaration of the mlp with the hyperparameters
        self.mlp = MLPClassifier( hidden_layer_sizes=self.hyper_parameters["hidden_layer_size"],
                                  max_iter=self.generation_number,
                                  activation= self.hyper_parameters["activation"],
                                  solver=self.hyper_parameters["solver"],
                                  learning_rate=self.hyper_parameters["learning_rate"],
                                  learning_rate_init= self.hyper_parameters["learning_rate_init"])

        # training of the mlp using the training set
        self.mlp.fit(self.training_data, ravel(self.training_labels))
        self.training_error = 1 - (self.mlp.score(self.training_data, ravel(self.training_labels)))

        # prediction of the risk labels using the validation set
        attack_risk_label_prediction = self.mlp.predict(self.validation_data)
        # measure the accurancy using the validation set
        self.validation_error = 1 - (accuracy_score(ravel(self.validation_labels), attack_risk_label_prediction))

        print(f"training_error {self.training_error}")
        print(f"validation_error {self.validation_error}")

        if self.is_initial_phase in ["Yes", "yes"]:

            # plot of the loss function in function of the number of generations
            plt.plot(self.mlp.loss_curve_)
            plt.xlabel("Number of Generations")
            plt.ylabel("Loss Function")
            plt.title("LOSS FUNCTION PLOT")
            plt.savefig("plots/loss_function_plot.png")
            plt.show()

            # creation of the confusion matrix plot
            confusion_mat = confusion_matrix(attack_risk_label_prediction, ravel(self.validation_labels), labels=self.mlp.classes_)
            display_confusion_matrix = ConfusionMatrixDisplay(confusion_matrix=confusion_mat, display_labels = self.mlp.classes_)
            display_confusion_matrix.plot()
            plt.savefig("plots/confusion_matrix.png")
            plt.show()

