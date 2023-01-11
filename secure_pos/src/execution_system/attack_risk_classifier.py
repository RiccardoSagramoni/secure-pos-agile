from data_objects.attack_risk_label import AttackRiskLabel


class AttackRiskClassifier:
    def __init__(self):
        self.__session_risk = None
        self.__monitoring_label = None

    def provide_attack_risk_level(self, classifier_model, prepared_session):
        self.__session_risk = classifier_model.predict(prepared_session)
        self.__monitoring_label = \
            AttackRiskLabel.ATTACK if self.__session_risk == 1 else AttackRiskLabel.NORMAL
        return self.__session_risk

    def attack_risk_label_converter(self, session_id: str):
        return {
            'session_id': session_id,
            'source': 'classifier',
            'value': self.__monitoring_label
        }
