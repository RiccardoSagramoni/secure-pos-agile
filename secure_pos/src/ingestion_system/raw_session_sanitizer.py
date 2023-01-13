from data_objects.raw_session import RawSession
from ingestion_system.configuration import Configuration
from validation.transaction_validator import TransactionValidator


class RawSessionSanitizer:
    """
    Class responsible for sanitizing a raw session, i.e. removing
    the invalid transactions from the session.
    """
    
    def __init__(self, raw_session: RawSession, conf: Configuration):
        """
        ``RawSessionSanitizer`` constructor.
        :param raw_session: raw session to sanitize
        :param conf: system configuration
        """
        self.__raw_session = raw_session
        self.__configuration = conf
    
    def remove_invalid_transactions(self) -> None:
        """
        Remove the transaction detected as "invalid" from the raw session.
        """
        self.__raw_session.transactions = (
            list(
                filter(
                    lambda t: TransactionValidator(t, self.__configuration).is_valid(),
                    self.__raw_session.transactions
                )
            )
        )
