import threading

import pandas

from database.DBManager import DBManager


class DatabaseController:
    _lock = threading.RLock()
    
    def __init__(self, db_path: str):
        self.database_manager = DBManager(db_path)
    
    def create_tables(self) -> None:
        with self._lock:
            # Table for commercial data
            self.database_manager.create_table(
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
            self.database_manager.create_table(
                "CREATE TABLE IF NOT EXISTS  geo ("
                "event_id TEXT PRIMARY KEY, "
                "session_id TEXT NOT NULL, "
                "loc_name BLOB, "
                "p_id BLOB,"
                "longitude BLOB,"
                "latitude BLOB"
                ")"
            )
            # Table for network data
            self.database_manager.create_table(
                "CREATE TABLE IF NOT EXISTS network ("
                "event_id TEXT PRIMARY KEY, "
                "session_id TEXT NOT NULL, "
                "ip BLOB"
                ")"
            )
            # Table for labels
            self.database_manager.create_table(
                "CREATE TABLE IF NOT EXISTS label ("
                "session_id TEXT PRIMARY KEY, "
                "label BLOB NOT NULL"
                ")"
            )
        return
    
    def insert_transaction_record(self, json_records: dict) -> bool:
        # Covert json record to dataframe
        df = pandas.DataFrame(json_records['data'])
        # Add information about session
        df['session_id'] = json_records['id']
        
        with self._lock:
            # Insert dataframe in db
            return self.database_manager.insert_dataframe(df, json_records['type'])
    
    def __check_session_records_presence(self, session_id: str, table: str) -> bool:
        with self._lock:
            data = self.database_manager.read_sql(
                f"SELECT event_id FROM {table} WHERE session_id = {session_id}"
            )
            return data is not None and not data.empty
    
    def __check_session_label_presence(self, session_id: str) -> bool:
        with self._lock:
            data = self.database_manager.read_sql(
                f"SELECT session_id FROM label WHERE session_id = {session_id}"
            )
            return data is not None and not data.empty
    
    def mockup_for_logic_of_development_or_monitoring(self): #TODO
        pass
    
    def check_if_session_is_completed(self, session_id: str):
        with self._lock:
            # Check if commercial, geo and network records exist
            ret = \
                self.__check_session_records_presence(session_id, 'commercial') \
                and self.__check_session_records_presence(session_id, 'geo') \
                and self.__check_session_records_presence(session_id, 'network')
            # Check if a human expert label is expected
            if self.mockup_for_logic_of_development_or_monitoring():
                ret = ret and self.__check_session_label_presence(session_id)
            # Return value
            return ret
