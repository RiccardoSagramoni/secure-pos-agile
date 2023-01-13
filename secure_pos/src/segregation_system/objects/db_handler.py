from threading import Semaphore

from database import DatabaseConnector


class DBHandler:
    """
    Class that manages the interactions with the DB
    """

    def __init__(self, path_db):
        self.path_db = path_db
        self.db_connection = DatabaseConnector(self.path_db)
        self.semaphore = Semaphore(1)

    def create_arrived_session_table(self):
        """
        Method that create the ArrivedSession table if not exists
        """
        # To avoid concurrency
        with self.semaphore:
            try:
                # If this is the first execution we have to create our table
                self.db_connection.create_table(
                    "CREATE TABLE IF NOT EXISTS ArrivedSessions"
                    "(id VARCHAR(80) PRIMARY KEY, time_mean FLOAT, time_median FLOAT,"
                    " time_std FLOAT, time_kurtosis FLOAT, time_skewness FLOAT, "
                    "amount_mean FLOAT, amount_median FLOAT, amount_std FLOAT, "
                    "amount_kurtosis FLOAT, amount_skewness FLOAT, type INT, label INT,"
                    "counter INT NOT NULL AUTOINCREMENT)")
            except Exception as ex:
                print(f"Exception during table creation execution: {ex}\n")

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
                print(f"Exception during insert execution: {ex}\n")
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
                print(f"Exception during extraction execution: {ex}\n")

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
                print(f"Exception during update execution: {ex}\n")

    def drop_records_testing(self, test_phase, sessions_vector):
        start_index = 0
        for i in range(test_phase):
            start_index += sessions_vector[i]
        end_index = sessions_vector[test_phase]
        with self.semaphore:
            try:
                self.db_connection.update("DELETE FROM ArrivedSessions "
                                          f"WHERE counter {start_index} " +
                                          f"AND {end_index};")

            except Exception as ex:
                print(f"Exception during db drop execution: {ex}\n")


