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
