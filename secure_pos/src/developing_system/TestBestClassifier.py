import joblib
from sklearn.metrics import accuracy_score
from pandas import read_csv
from numpy import ravel

from developing_system.GridSearchController import GridSearchController
from developing_system.TrainingConfiguration import TrainingConfiguration

class TestBestClassifier:


    def __init__(self, training_conf:TrainingConfiguration):

        self.test_tolerance = training_conf.test_tolerance
        self.id_best_classifier = training_conf.best_classifier_number
        self.test_data = read_csv('prova/testingData.csv')
        self.test_labels = read_csv('prova/testingLabels.csv')
        self.test_error = None


    def test_best_classifier(self, path_mlp_to_test):

        loaded_classifier = joblib.load(path_mlp_to_test)
        # prediction of the risk labels using the test set
        attack_risk_label_prediction = loaded_classifier.predict(self.test_data)
        # measure the accurancy using the validation set
        self.test_error = 1 - (accuracy_score(ravel(self.test_labels), attack_risk_label_prediction))


    def print(self):
        print("*********************************")
        print(f"id_best_classifier:{self.id_best_classifier}")
        print(f"test_tolerance:{self.test_tolerance}")
        print(f"test_error:{self.test_error}")
        print("*********************************")

