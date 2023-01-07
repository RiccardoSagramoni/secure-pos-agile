from data_objects.attack_risk_label import AttackRiskLabel
from data_objects.raw_session import RawSession


class RawSessionConverter:
    
    def __init__(self, raw_session: RawSession):
        self.__raw_session = raw_session
    
    def convert_to_dict(self) -> dict:
        doc = {
            'session_id': self.__raw_session.session_id,
            'attack_risk_label': self.__raw_session.attack_risk_label,
            'transactions': []
        }
        for t in self.__raw_session.transactions:
            doc['transactions'].append(vars(t))
        return doc


class AttackRiskLabelConverter:
    
    def __init__(self, session_id: str, label: AttackRiskLabel):
        self.__session_id = session_id
        self.__label = label
    
    def convert_to_dict(self) -> dict:
        return {
            'session_id': self.__session_id,
            'source': 'expert',
            'value': self.__label.value
        }
