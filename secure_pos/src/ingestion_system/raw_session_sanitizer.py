from data_objects.raw_session import RawSession


class RawSessionSanitizer:
    
    def __init__(self, raw_session: RawSession):
        self.__raw_session = raw_session
    
    def remove_invalid_transactions(self):
        self.__raw_session.transactions = (
            list(
                filter(
                    lambda t: t.is_valid(),
                    self.__raw_session.transactions
                )
            )
        )
