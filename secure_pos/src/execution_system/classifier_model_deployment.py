import os.path

import joblib
from sklearn.neural_network import MLPClassifier

from execution_system.communication_controller import CLASSIFIER_MODEL_PATH
from utility import data_folder


class ClassifierModelDeployment:
    __classifier_model = None

    def __init__(self):
        pass

    def load_classifier_model(self) -> None:
        """
        Start the classifier model
        """
        self.__classifier_model = joblib.load(os.path.join(data_folder, CLASSIFIER_MODEL_PATH))

    def get_classifier_model(self) -> MLPClassifier:
        """
        Get the classifier deployed and loaded
        :return: the classifier model
        """
        return self.__classifier_model
