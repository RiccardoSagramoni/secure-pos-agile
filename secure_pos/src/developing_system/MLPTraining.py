from sklearn.neural_network import MLPClassifier
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay, accuracy_score
from pandas import read_csv
from numpy import ravel
import matplotlib.pyplot as plt

class MLPTraining:

    def __init__(self):

        self.is_initial_phase = True
        self.mlp = None
        self.first_hidden_layer_size = None
        self.generation_number = 2000
        self.activation = None
        self.solver = None
        self.learning_rate = None
        self.random_state = None
        self.training_data = read_csv('prova/trainingData.csv')
        self.training_labels=read_csv('prova/trainingLabels.csv')
        self.validation_data = read_csv('prova/testingData.csv')
        self.validation_labels = read_csv('prova/testingLabels.csv')
        self.validation_error = None


    def set_hyperparameters(self, is_initial_phase, first_hidden_layer_size, activation, solver, learning_rate_mode):

        self.is_initial_phase = is_initial_phase
        self.first_hidden_layer_size = first_hidden_layer_size
        self.activation = activation
        self.solver = solver
        self.learning_rate = learning_rate_mode


    def train_neural_network(self):

        # declaration of the mlp with the hyperparameters
        self.mlp = MLPClassifier( hidden_layer_sizes=self.first_hidden_layer_size, max_iter=self.generation_number,
                                  activation= self.activation, solver= self.solver, learning_rate=self.learning_rate)
        # training of the mlp using the training set
        self.mlp.fit(self.training_data, ravel(self.training_labels))
        # prediction of the risk labels using the validation set
        attack_risk_label_prediction = self.mlp.predict(self.validation_data)

        if self.is_initial_phase:

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

        # measure the accurancy using the validation set
        self.validation_error = accuracy_score(ravel(self.validation_labels), attack_risk_label_prediction)
        print(f"Validation Error:{self.validation_error}")


# classifier = MLPTraining()
# classifier.set_hyperparameters(is_initial_phase = True, first_hidden_layer_size = 80, activation = 'relu', solver = 'adam', learning_rate_mode = 'constant')
# classifier.train_neural_network()