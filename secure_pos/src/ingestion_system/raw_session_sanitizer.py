from data_objects.raw_session import RawSession
from ingestion_system.configuration import Configuration
from validation.transaction_validator import TransactionValidator


class RawSessionSanitizer:
    
    def __init__(self, raw_session: RawSession, conf: Configuration):
        self.__raw_session = raw_session
        self.__configuration = conf
    
    def remove_invalid_transactions(self) -> None:
        self.__raw_session.transactions = (
            list(
                filter(
                    lambda t: TransactionValidator(t, self.__configuration).is_valid(),
                    self.__raw_session.transactions
                )
            )
        )
