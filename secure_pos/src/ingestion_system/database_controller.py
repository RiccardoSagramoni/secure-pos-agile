import threading

import pandas

from data_objects.raw_session import RawSession
from database.DBManager import DBManager
from factory.raw_session_factory import RawSessionFactory
from ingestion_system.configuration import Configuration
from ingestion_system.system_mode_tracker import SystemModeTracker


class DatabaseController:
    __lock = threading.RLock()
    
    def __init__(self, conf: Configuration, tracker: SystemModeTracker):
        self.__database_connector = DBManager(conf.database_path)
        self.__system_mode_tracker = tracker
        self.__create_tables()
    
    def __create_tables(self) -> None:
        with self.__lock:
            # Table for commercial data
            self.__database_connector.create_table(
                "CREATE TABLE IF NOT EXISTS commercial ("
                "event_id TEXT PRIMARY KEY, "
                "session_id TEXT NOT NULL,"
                "cardid TEXT,"
                "posid TEXT,"
                "posname TEXT,"
                "date TEXT,"
                "time TEXT,"
                "payment_type TEXT,"
                "payment_circuit TEXT,"
                "amount TEXT,"
                "currency TEXT"
                ")"
            )
            # Table for geo data
            self.__database_connector.create_table(
                "CREATE TABLE IF NOT EXISTS geo ("
                "event_id TEXT PRIMARY KEY, "
                "session_id TEXT NOT NULL, "
                "loc_name TEXT, "
                "p_id TEXT,"
                "longitude TEXT,"
                "latitude TEXT"
                ")"
            )
            # Table for network data
            self.__database_connector.create_table(
                "CREATE TABLE IF NOT EXISTS network ("
                "event_id TEXT PRIMARY KEY, "
                "session_id TEXT NOT NULL, "
                "ip TEXT"
                ")"
            )
            # Table for labels
            self.__database_connector.create_table(
                "CREATE TABLE IF NOT EXISTS label ("
                "session_id TEXT PRIMARY KEY, "
                "label TEXT NOT NULL"
                ")"
            )
    
    #
    def insert_transaction_record(self, json_records: dict) -> bool:
        # Covert json record to dataframe
        data_content = json_records['data']
        if type(data_content) is list:
            df = pandas.DataFrame(data_content)
        elif type(data_content) is dict:
            df = pandas.DataFrame(data_content, [0])
            df = df.drop(columns='event_id')
        else:
            raise ValueError("json records data not in valid format")
        
        # Add information about session
        df['session_id'] = json_records['session_id']
        
        with self.__lock:
            # Insert dataframe in db
            return self.__database_connector.insert(df, json_records['type'])
    
    #
    def __check_session_records_presence(self, session_id: str, table: str) -> bool:
        with self.__lock:
            data = self.__database_connector.read_sql(
                f"SELECT event_id FROM {table} WHERE session_id = '{session_id}'"
            )
        return data is not None and not data.empty
    
    #
    def __check_session_label_presence(self, session_id: str) -> bool:
        with self.__lock:
            data = self.__database_connector.read_sql(
                f"SELECT session_id FROM label WHERE session_id = '{session_id}'"
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
            # Get raw session data
            raw_session_df = self.__database_connector.read_sql(
                "SELECT * "
                "FROM commercial "
                "INNER JOIN geo USING (event_id) "
                "INNER JOIN network USING (event_id) "
                f"WHERE commercial.session_id = '{session_id}';"
            )
            # Read label value for this session
            label_df = self.__database_connector.read_sql(
                f"SELECT label FROM label WHERE session_id = '{session_id}';"
            )
            # Check if label exist
            if label_df.empty:
                label = None
            else:
                label = label_df['label'][0]
        return RawSessionFactory.generate_from_dataframe(session_id, raw_session_df, label)
    
    def __delete_records(self, session_id: str, table: str) -> None:
        with self.__lock:
            self.__database_connector.update(
                f"DELETE FROM {table} "
                f"WHERE session_id = '{session_id}';"
            )

    def drop_raw_session(self, session_id: str) -> None:
        with self.__lock:
            self.__delete_records(session_id, 'commercial')
            self.__delete_records(session_id, 'geo')
            self.__delete_records(session_id, 'network')
            self.__delete_records(session_id, 'label')
