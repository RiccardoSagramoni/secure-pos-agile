import os

import joblib
from sklearn.neural_network import MLPClassifier

from execution_system.communication_controller import CLASSIFIER_MODEL_PATH
from utility import data_folder


class ClassifierModelDeployment:
    __classifier_model = None

    def __init__(self):
        pass

    def load_classifier_model(self) -> None:
        self.__classifier_model = joblib.load(os.path.join(data_folder, CLASSIFIER_MODEL_PATH))

    def get_classifier_model(self) -> MLPClassifier:
        return self.__classifier_model
