import joblib

from execution_system.communication_controller import CLASSIFIER_MODEL_PATH


class DeployedClassifierModel:
    __classifier_model = None

    def __init__(self):
        pass

    def load_classifier_model(self):
        self.__classifier_model = joblib.load(CLASSIFIER_MODEL_PATH)

    def get_classifier_model(self):
        return self.__classifier_model
