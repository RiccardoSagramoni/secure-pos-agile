import logging
import threading
import typing

from data_objects.raw_session import RawSession
from ingestion_system.database_controller import DatabaseController


class RecordSynchronizer:
    __lock = threading.RLock()
    
    def __init__(self, db_controller: DatabaseController):
        self.__database_controller = db_controller
    
    def try_session_synchronization(self, json_records: dict) -> typing.Optional[RawSession]:
        with self.__lock:
            # Check if we have all the necessary data of the session
            session_id = json_records['id']
            if not self.__database_controller.is_session_completed(session_id):
                return None
            
            # Get raw session and remove it from database
            raw_session = self.__database_controller.get_raw_session(session_id)
            self.__database_controller.drop_raw_session(session_id)
            return raw_session
