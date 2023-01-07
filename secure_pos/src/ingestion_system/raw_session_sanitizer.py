from data_objects.raw_session import RawSession
from ingestion_system.configuration import Configuration


class RawSessionSanitizer:
    
    def __init__(self, raw_session: RawSession, conf: Configuration):
        self.raw_session = raw_session
        self.configuration = conf
    
    def remove_invalid_transactions(self):
        self.raw_session.transactions = (
            list(
                filter(
                    lambda t: t.is_valid(),
                    self.raw_session.transactions
                )
            )
        )
    
    def does_session_have_enough_transactions(self):
        # TODO maybe move it to another class?
        pass
