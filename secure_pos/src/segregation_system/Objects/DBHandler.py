from threading import Semaphore

from database.DBManager import DBManager


class DBHandler:
    """
    Class that manages the interactions with the DB
    """

    def __init__(self, path_db):
        self.path_db = path_db
        self.db_connection = DBManager(self.path_db)
        self.semaphore = Semaphore(1)

    def create_arrived_session_table(self):
        """
        Method that create the ArrivedSession table if not exists
        """
        # To avoid concurrency
        with self.semaphore:
            # If this is the first execution we have to create our table
            self.db_connection.create_table(
                "CREATE TABLE IF NOT EXISTS ArrivedSessions"
                "(id VARCHAR(80) PRIMARY KEY, time_mean FLOAT, time_median FLOAT, time_std FLOAT,"
                "time_kurtosis FLOAT, time_skewness FLOAT, amount_mean FLOAT, amount_median FLOAT,"
                " amount_std FLOAT, amount_kurtosis FLOAT, amount_skewness FLOAT, "
                "type INT, label INT)")

    def insert_session(self, data_frame) -> bool:
        """
        Method that insert the new received session inside the DB
        :param data_frame: received session
        :return: boolean
        """
        with self.semaphore:
            try:
                ret = self.db_connection.insert(data_frame, 'ArrivedSessions')
            except Exception as ex:
                print("Exception during query execution: %s\n",ex)
            return ret

    def extract_all_unallocated_data(self):
        """
        Method that perform a query for unused data extraction
        :return: Array of unused data
        """
        # Paying attention to critical runs
        with self.semaphore:
            try:
                # Extracts data
                features = self.db_connection.read_sql('SELECT time_mean, time_median, time_std,'
                                                       'time_kurtosis, time_skewness, amount_mean,'
                                                       'amount_median, amount_std, amount_kurtosis,'
                                                       'amount_skewness, id FROM ArrivedSessions '
                                                       'WHERE type = -1')
                # Extracts labels for current data
                labels = self.db_connection.read_sql('SELECT label '
                                                     'FROM ArrivedSessions '
                                                     'WHERE type = -1')
            except Exception as ex:
                print("Exception during query execution: %s\n",ex)

        return [features, labels]

    def update_type(self):
        """
        Update the type and mark the sessions as used on the DB
        """
        with self.semaphore:
            try:
                self.db_connection.update("UPDATE ArrivedSessions "
                                          "SET type = 0 "
                                          "WHERE type = -1")
            except Exception as ex:
                print("Exception during query execution: %s\n", ex)
