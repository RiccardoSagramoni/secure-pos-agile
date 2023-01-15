import pandas as pd
from sklearn.neural_network import MLPClassifier

from data_objects.attack_risk_label import AttackRiskLabel


class AttackRiskClassifier:
    """
    Class responsible for the execution of the classifier model,
    i.e. generating the attack risk level for a session.
    """
    __session_risk = None
    __monitoring_label = None

    def __init__(self, classifier_model: MLPClassifier, session_id: str, prepared_session: pd.DataFrame):
        """
        Constructor of the `AttackRiskClassifier` class
        :classifier_model: the MLPClassifier to execute
        :session_id: id of the session to classify
        :prepared_session: session to classify
        """
        self.__classifier_model = classifier_model
        self.__session_id = session_id
        self.__prepared_session = prepared_session

    def provide_attack_risk_level(self) -> str:
        """
        Execute the classifier and get the risk level
        :return: the attack risk level detected ('1' for ATTACK, '0' for NORMAL)
        """
        print("get attack risk")
        self.__session_risk = self.__classifier_model.predict(self.__prepared_session)[0]
        print(self.__session_risk)
        self.__monitoring_label = \
            AttackRiskLabel.ATTACK if self.__session_risk == '1' else AttackRiskLabel.NORMAL
        return self.__session_risk

    def attack_risk_label_converter(self) -> dict:
        """
        Class responsible for converting the attack risk level label in a JSON object,
        in order to send it to the monitoring system.
        :return: the label to send
        """
        return {
            'session_id': self.__session_id,
            'source': 'classifier',
            'value': self.__monitoring_label.value
        }
