import joblib
from sklearn.metrics import accuracy_score
from numpy import ravel

from development_system.training_configuration import TrainingConfiguration
from development_system.machine_learning_sets_archiver import MachineLearningSetsArchiver
from development_system.test_best_classifier_report_generator import TestBestCLassifierReportGenerator

TEST_SETS = 2

class TestBestClassifier:


    def __init__(self, training_conf: TrainingConfiguration, training_error_best_classifier, ml_sets_archive_handler: MachineLearningSetsArchiver):

        [test_data, test_labels] = ml_sets_archive_handler.get_ml_sets(TEST_SETS)

        self.test_tolerance = training_conf.test_tolerance
        self.id_best_classifier = training_conf.best_classifier_number
        self.test_data = test_data
        self.test_labels = test_labels
        self.training_error = training_error_best_classifier
        self.test_error = None


    def test_best_classifier(self, path_mlp_to_test):

        loaded_classifier = joblib.load(path_mlp_to_test)
        # prediction of the risk labels using the test set
        attack_risk_label_prediction = loaded_classifier.predict(self.test_data)
        # measure the accurancy using the validation set
        self.test_error = 1 - (accuracy_score(ravel(self.test_labels), attack_risk_label_prediction))

        TestBestCLassifierReportGenerator.generate_report(self.test_tolerance, self.id_best_classifier, self.training_error, self.test_error)


