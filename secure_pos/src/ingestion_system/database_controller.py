import threading

import pandas

from data_objects.raw_session import RawSession
from database import DatabaseConnector
from factory.raw_session_factory import RawSessionFactory
from ingestion_system.configuration import Configuration
from ingestion_system.system_mode_tracker import SystemModeTracker


class DatabaseController:
    """
    Class responsible for handling all the accesses to the database API.
    All methods are thread-safe.
    """
    __lock = threading.RLock()
    
    def __init__(self, conf: Configuration, tracker: SystemModeTracker):
        self.__system_mode_tracker = tracker
        self.__database_connector = DatabaseConnector(conf.database_path)
        self.__database_connector.drop_database()
        self.__create_tables()
    
    def __create_tables(self) -> None:
        """
        Create the table for storing the records in the db.
        A table for each type of record (commercial, geo, network, label) is generated.
        """
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
    
    def insert_transaction_record(self, json_records: dict) -> bool:
        """
        Insert a transaction record (commercial, geo, network, label) in the db.
        :param json_records: records to insert in json format.
        :return: True if the insert query was successful, False otherwise.
        """
        # Covert json record to dataframe
        data_content = json_records['data']
        if isinstance(data_content, list):
            dataframe = pandas.DataFrame(data_content)
        elif isinstance(data_content, dict):
            dataframe = pandas.DataFrame(data_content, [0])
            dataframe = dataframe.drop(columns='event_id')
        else:
            raise ValueError("json records data not in valid format")
        
        # Add information about session
        dataframe['session_id'] = json_records['session_id']
        
        with self.__lock:
            # Insert dataframe in db
            return self.__database_connector.insert(dataframe, json_records['type'])
    
    def __check_session_records_presence(self, session_id: str, table: str) -> bool:
        """
        Check if the database contains a specified type of records of a specified session.
        :param session_id: id of the session
        :param table: name of the table where to look for the records.
        :return: True if the records are in the db, False otherwise
        """
        with self.__lock:
            data = self.__database_connector.read_sql(
                f"SELECT event_id FROM {table} WHERE session_id = '{session_id}'"
            )
        return data is not None and not data.empty
    
    def __check_session_label_presence(self, session_id: str) -> bool:
        """
        Check if the database contains the label of a specified session.
        :param session_id: id of the session
        :return: True if the label is in the db, False otherwise
        """
        with self.__lock:
            data = self.__database_connector.read_sql(
                f"SELECT session_id FROM label WHERE session_id = '{session_id}'"
            )
        return data is not None and not data.empty
    
    def is_session_completed(self, session_id: str) -> bool:
        """
        Check if a session is completed, i.e. if it has all the necessary
        transaction records.
        :param session_id: id of the session
        :return: True if the session is completed, False otherwise
        """
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
        """
        Read the database and generate a raw session.
        :param session_id: id of the session to generate
        :return: the generated RawSession object
        """
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
        # Generate raw session
        return RawSessionFactory.generate_from_dataframe(session_id, raw_session_df, label)
    
    def __delete_records(self, session_id: str, table: str) -> None:
        """
        Delete the records of a session from a specified table.
        :param session_id: id of the session
        :param table: name of the table
        """
        with self.__lock:
            self.__database_connector.update(
                f"DELETE FROM {table} "
                f"WHERE session_id = '{session_id}';"
            )

    def drop_raw_session(self, session_id: str) -> None:
        """
        Remove the data of a raw session.
        :param session_id: id of the session.
        """
        with self.__lock:
            self.__delete_records(session_id, 'commercial')
            self.__delete_records(session_id, 'geo')
            self.__delete_records(session_id, 'network')
            self.__delete_records(session_id, 'label')
