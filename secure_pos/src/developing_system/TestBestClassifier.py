import joblib
from sklearn.metrics import accuracy_score
from numpy import ravel

from developing_system.TrainingConfiguration import TrainingConfiguration
from developing_system.MachineLearningSetsArchiver import MachineLearningSetsArchiver
from developing_system.TestBestClassifierReportGenerator import TestBestCLassifierReportGenerator

class TestBestClassifier:


    def __init__(self, training_conf: TrainingConfiguration, training_error_best_classifier, ml_sets_archive_handler: MachineLearningSetsArchiver):

        self.test_tolerance = training_conf.test_tolerance
        self.id_best_classifier = training_conf.best_classifier_number
        self.test_data = ml_sets_archive_handler.get_ml_sets(2, False)
        self.test_labels = ml_sets_archive_handler.get_ml_sets(2, True)
        self.training_error = training_error_best_classifier
        self.test_error = None


    def test_best_classifier(self, path_mlp_to_test):

        loaded_classifier = joblib.load(path_mlp_to_test)
        # prediction of the risk labels using the test set
        attack_risk_label_prediction = loaded_classifier.predict(self.test_data)
        # measure the accurancy using the validation set
        self.test_error = 1 - (accuracy_score(ravel(self.test_labels), attack_risk_label_prediction))

        TestBestCLassifierReportGenerator().generate_report(self)


    def print(self):
        print("*********************************")
        print(f"id_best_classifier:{self.id_best_classifier}")
        print(f"test_tolerance:{self.test_tolerance}")
        print(f"test_error:{self.test_error}")
        print("*********************************")

