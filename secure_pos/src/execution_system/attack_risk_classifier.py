import pandas as pd
from sklearn.neural_network import MLPClassifier

from data_objects.attack_risk_label import AttackRiskLabel


class AttackRiskClassifier:
    __session_risk = None
    __monitoring_label = None

    def __init__(self, classifier_model: MLPClassifier, session_id: str, prepared_session: pd.DataFrame):
        self.__classifier_model = classifier_model
        self.__session_id = session_id
        self.__prepared_session = prepared_session

    def provide_attack_risk_level(self):
        self.__session_risk = self.__classifier_model.predict(self.__prepared_session)
        self.__monitoring_label = \
            AttackRiskLabel.ATTACK if self.__session_risk == 1 else AttackRiskLabel.NORMAL
        return self.__session_risk

    def attack_risk_label_converter(self):
        return {
            'session_id': self.__session_id,
            'source': 'classifier',
            'value': self.__monitoring_label
        }
