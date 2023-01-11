import joblib

CLASSIFIER_MODEL_PATH = "execution_system/classifier_model.sav"


class ExecutionSystemDeployment:
    def __init__(self):
        self.__classifier_model = None

    def load_classifier_model(self):
        self.__classifier_model = joblib.load(CLASSIFIER_MODEL_PATH)

    def get_classifier_model(self):
        return self.__classifier_model
