from threading import Semaphore

from database.DBManager import DBManager

class MachineLearningSetsArchiver:

    def __init__(self, database_path):

        self.database_path = database_path
        self.db_connection = DBManager(self.database_path)
        self.semaphore = Semaphore(1)


    def create_ml_sets_table(self):

        with self.semaphore:
            self.db_connection.create_table(
                "CREATE TABLE IF NOT EXISTS MachineLearningSets"
                "(id VARCHAR(80) PRIMARY KEY, time_mean FLOAT, time_median FLOAT, time_std FLOAT,"
                "time_kurtosis FLOAT, time_skewness FLOAT, amount_mean FLOAT, amount_median FLOAT, amount_std FLOAT,"
                "amount_kurtosis FLOAT, amount_skewness FLOAT, "
                "type INT, label VARCHAR(20))"
            )

    def drop_ml_sets_db(self):
        with self.semaphore:
            self.db_connection.delete_table("MachineLearningSets")
            self.db_connection.drop_database()


    def insert_ml_sets(self, data_frame):

        with self.semaphore:
            try:
                ret = self.db_connection.insert(data_frame, 'MachineLearningSets')
            except Exception as ex:
                print("Error during the insert execution: %s", ex)
            return ret

    def get_ml_sets(self, type_of_set):

        with self.semaphore:
            try:
                label_set = self.db_connection.read_sql("SELECT label "
                                                        "FROM MachineLearningSets "
                                                        f"WHERE type = '{type_of_set}'")

                data_set = self.db_connection.read_sql("SELECT time_mean, time_median, time_std,"
                                                        "time_kurtosis, time_skewness, amount_mean,"
                                                        "amount_median, amount_std, amount_kurtosis,"
                                                        "amount_skewness FROM MachineLearningSets "
                                                        f"WHERE type = '{type_of_set}'")
            except Exception as ex:
                print("Error during the query execution of the ml_sets: %s", ex)
            return [data_set, label_set]

