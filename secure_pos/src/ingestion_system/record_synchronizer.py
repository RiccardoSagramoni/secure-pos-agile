import threading
import typing

from data_objects.raw_session import RawSession
from ingestion_system.database_controller import DatabaseController


class RecordSynchronizer:
    """
    Class responsible for the synchronization of the records
    belonging to the same raw session.
    All methods are thread-safe.
    """
    __lock = threading.RLock()
    
    def __init__(self, db_controller: DatabaseController):
        self.__database_controller = db_controller
    
    def try_session_synchronization(self, session_id: str) -> typing.Optional[RawSession]:
        """
        Try to synchronize a session.
        A session can be synchronized only if all the required records
        have been received by the system (i.e. the session was completed).
        :param session_id: id of the session
        :return: a RawSession object if the synchronization was successful, None otherwise
        """
        with self.__lock:
            # Check if we have all the necessary data of the session
            try:
                if not self.__database_controller.is_session_completed(session_id):
                    return None
            except ValueError:
                return None
            
            # Get raw session and remove it from database
            raw_session = self.__database_controller.get_raw_session(session_id)
            self.__database_controller.drop_raw_session(session_id)
            return raw_session
