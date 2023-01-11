import jsons

from data_objects.attack_risk_label import AttackRiskLabel
from data_objects.raw_session import RawSession


class RawSessionPackager:
    """
    Class responsible for packaging a RawSession object in a JSON object,
    in order to send it to the preparation system.
    """
    
    def __init__(self, raw_session: RawSession):
        self.__raw_session = raw_session
    
    def package_as_json_dict(self) -> dict:
        doc = {
            'session_id': self.__raw_session.session_id,
            'attack_risk_label': self.__raw_session.attack_risk_label.value,
            'transactions': []
        }
        for transaction in self.__raw_session.transactions:
            doc['transactions'].append(
                jsons.dump(transaction)
            )
        return doc


class AttackRiskLabelPackager:
    """
    Class responsible for packaging a AttackRiskLabel object in a JSON object,
    in order to send it to the monitoring system.
    """
    
    def __init__(self, session_id: str, label: AttackRiskLabel):
        self.__session_id = session_id
        self.__label = label
    
    def package_as_json_dict(self) -> dict:
        return {
            'session_id': self.__session_id,
            'source': 'expert',
            'value': self.__label.value
        }
