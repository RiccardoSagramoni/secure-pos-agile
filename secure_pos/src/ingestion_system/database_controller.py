import threading

import pandas

from data_objects.raw_session import RawSession
from database.DBManager import DBManager
from ingestion_system.configuration import Configuration
from ingestion_system.system_mode_tracker import SystemModeTracker


class DatabaseController:
    __lock = threading.RLock()
    
    def __init__(self, conf: Configuration, tracker: SystemModeTracker):
        self.__database_manager = DBManager(conf.database_path)
        self.__system_mode_tracker = tracker
    
    def create_tables(self) -> None:
        with self.__lock:
            # Table for commercial data
            self.__database_manager.create_table(
                "CREATE TABLE IF NOT EXISTS commercial ("
                "event_id TEXT PRIMARY KEY, "
                "session_id TEXT NOT NULL,"
                "cardid BLOB,"
                "posid BLOB,"
                "date BLOB,"
                "time BLOB,"
                "payment_type BLOB,"
                "payment_circuit BLOB,"
                "amount BLOB,"
                "currency BLOB"
                ")"
            )
            # Table for geo data
            self.__database_manager.create_table(
                "CREATE TABLE IF NOT EXISTS geo ("
                "event_id TEXT PRIMARY KEY, "
                "session_id TEXT NOT NULL, "
                "loc_name BLOB, "
                "p_id BLOB,"
                "longitude BLOB,"
                "latitude BLOB"
                ")"
            )
            # Table for network data
            self.__database_manager.create_table(
                "CREATE TABLE IF NOT EXISTS network ("
                "event_id TEXT PRIMARY KEY, "
                "session_id TEXT NOT NULL, "
                "ip BLOB"
                ")"
            )
            # Table for labels
            self.__database_manager.create_table(
                "CREATE TABLE IF NOT EXISTS label ("
                "session_id TEXT PRIMARY KEY, "
                "label BLOB NOT NULL"
                ")"
            )
    
    #
    def insert_transaction_record(self, json_records: dict) -> bool:
        # Covert json record to dataframe
        df = pandas.DataFrame(json_records['data'])
        # Add information about session
        df['session_id'] = json_records['id']
        
        with self.__lock:
            # Insert dataframe in db
            return self.__database_manager.insert_dataframe(df, json_records['type'])
    
    #
    def __check_session_records_presence(self, session_id: str, table: str) -> bool:
        with self.__lock:
            data = self.__database_manager.read_sql(
                f"SELECT event_id FROM {table} WHERE session_id = {session_id}"
            )
        return data is not None and not data.empty
    
    #
    def __check_session_label_presence(self, session_id: str) -> bool:
        with self.__lock:
            data = self.__database_manager.read_sql(
                f"SELECT session_id FROM label WHERE session_id = {session_id}"
            )
        return data is not None and not data.empty
    
    #
    def is_session_completed(self, session_id: str) -> bool:
        with self.__lock:
            # Check if commercial, geo and network records exist
            ret = \
                self.__check_session_records_presence(session_id, 'commercial') \
                and self.__check_session_records_presence(session_id, 'geo') \
                and self.__check_session_records_presence(session_id, 'network')
            # Check if a human expert label is expected
            if self.__system_mode_tracker.is_label_required(session_id):
                ret = ret and self.__check_session_label_presence(session_id)
        # Return value
        return ret

    def get_raw_session(self, session_id: str) -> RawSession:
        with self.__lock:
            raw_session_df = self.__database_manager.read_sql(
                "SELECT * "
                "FROM commercial "
                "INNER JOIN geo USING (event_id) "
                "INNER JOIN network USING (event_id) "
                f"WHERE session_id = {session_id};"
            )
            label = self.__database_manager.read_sql(
                f"SELECT label FROM label WHERE session_id = {session_id};"
            )['label'][0]  # todo da testare con debugger!!!
            return RawSession(session_id, raw_session_df, label)
    
    def __delete_records(self, session_id: str, table: str) -> None:
        with self.__lock:
            self.__database_manager.update(
                f"DELETE FROM {table}"
                f"WHERE session_id = {session_id};"
            )

    def drop_raw_session(self, session_id: str) -> None:
        with self.__lock:
            self.__delete_records(session_id, 'commercial')
            self.__delete_records(session_id, 'geo')
            self.__delete_records(session_id, 'network')
            self.__delete_records(session_id, 'label')
