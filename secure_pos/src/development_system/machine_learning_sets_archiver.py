import json
import pandas as pd
from threading import Semaphore

from database import DatabaseConnector


class MachineLearningSetsArchiver:

    def __init__(self, database_path):

        self.database_path = database_path
        self.db_connection = DatabaseConnector(self.database_path)
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

    def create_json_received_table(self):
        with self.semaphore:
            self.db_connection.create_table(
                "CREATE TABLE IF NOT EXISTS JsonDataReceived "
                "(id_classifier INTEGER PRIMARY KEY AUTOINCREMENT, sets TEXT NOT NULL)"
            )

    def drop_ml_sets_table(self):
        with self.semaphore:
            self.db_connection.delete_table("MachineLearningSets")

    def insert_ml_sets(self):

        self.create_ml_sets_table()
        with self.semaphore:

            ml_sets = self.db_connection.read_sql("SELECT sets "
                                                  "FROM JsonDataReceived "
                                                  "LIMIT 1")

            self.db_connection.update("DELETE FROM JsonDataReceived WHERE id_classifier = ("
                                      "SELECT Min(id_classifier) FROM JsonDataReceived)")

            json_data_ml_sets = json.loads(ml_sets.at[0, 'sets'])
            data_frame = pd.DataFrame(json_data_ml_sets,
                                      columns=['id', 'time_mean', 'time_median', 'time_std',
                                               'time_kurtosis', 'time_skewness', 'amount_mean',
                                               'amount_median', 'amount_std', 'amount_kurtosis',
                                               'amount_skewness', 'type', 'label'])

            try:
                ret = self.db_connection.insert(data_frame, 'MachineLearningSets')
            except Exception as ex:
                ret = 0
                print("Error during the insert execution in MachineLearningSets: %s", ex)
            return ret

    def insert_json_received(self, data_frame):

        with self.semaphore:
            try:
                ret = self.db_connection.insert(data_frame, 'JsonDataReceived')
            except Exception as ex:
                ret = 0
                print("Error during the insert execution in JsonDataReceived: %s", ex)
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
