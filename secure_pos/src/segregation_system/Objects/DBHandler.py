import sys
from threading import Semaphore
import numpy as np

from database.DBManager import DBManager


class DBHandler:

    def __init__(self, path_db):
        self.path_db = path_db
        self.db_connection = DBManager(self.path_db)
        self.semaphore = Semaphore(1)

    def create_arrived_session_table(self):
        # To avoid concurrency
        self.semaphore.acquire()
        # If this is the first execution we have to create our table
        self.db_connection.create_table(
            "CREATE TABLE IF NOT EXISTS ArrivedSessions"
            "(id VARCHAR(80) PRIMARY KEY, time_mean FLOAT, time_median FLOAT, time_std FLOAT,"
            "time_kurtosis FLOAT, time_skewness FLOAT, amount_mean FLOAT, amount_median FLOAT,"
            " amount_std FLOAT, amount_kurtosis FLOAT, amount_skewness FLOAT, "
            "type INT, label VARCHAR(20))")
        self.semaphore.release()

    def insert_session(self, data_frame):
        self.semaphore.acquire()
        ret = self.db_connection.insert(data_frame, 'ArrivedSessions')
        self.semaphore.release()
        return ret

    def extract_all_unallocated_data(self):
        # Paying attention to critical runs
        self.semaphore.acquire()
        # Extracts data
        features = self.db_connection.read_sql('SELECT time_mean, time_median, time_std,'
                                               'time_kurtosis, time_skewness, amount_mean,'
                                               'amount_median, amount_std, amount_kurtosis,'
                                               'amount_skewness FROM ArrivedSessions '
                                               'WHERE type = 0')
        # Extracts labels for current data
        labels = self.db_connection.read_sql('SELECT label FROM ArrivedSessions WHERE type = 0')
        self.semaphore.release()

        return [features, labels]

    def normalize_current_data(self):
        # Get data
        data_frame = self.extract_to_be_normalized_data()

        # Exclude id that have not to be normalized
        my_cols = set(data_frame.columns)
        my_cols.remove('id')
        features = data_frame[list(my_cols)]

        # Normalize
        normalized_df = (features - features.min()) / (features.max() - features.min())
        normalized_df['id'] = data_frame['id']

        for _id in normalized_df['id']:
            row = []
            row = np.where(normalized_df.id == _id)
            self.db_connection.update("UPDATE ArrivedSessions SET "
                                      "time_mean = " + str(normalized_df.loc[row[0][0]]['time_mean']) +
                                      ", time_std = " + str(normalized_df.loc[row[0][0]]['time_std']) +
                                      ", time_skewness = " + str(normalized_df.loc[row[0][0]]['time_skewness']) +
                                      ", time_median = " + str(normalized_df.loc[row[0][0]]['time_median']) +
                                      ", time_kurtosis = " + str(normalized_df.loc[row[0][0]]['time_kurtosis']) +
                                      ", amount_mean = " + str(normalized_df.loc[row[0][0]]['amount_mean']) +
                                      ", amount_std = " + str(normalized_df.loc[row[0][0]]['amount_std']) +
                                      ", amount_median = " + str(normalized_df.loc[row[0][0]]['amount_median']) +
                                      ", amount_skewness = " + str(normalized_df.loc[row[0][0]]['amount_skewness']) +
                                      ", amount_kurtosis = " + str(normalized_df.loc[row[0][0]]['amount_kurtosis']) +
                                      ", type = 0 WHERE id = '" + _id + "'")

    def extract_to_be_normalized_data(self):
        # Paying attention to critical runs
        self.semaphore.acquire()
        # Extracts data
        features = self.db_connection.read_sql('SELECT id, time_mean, time_median, time_std,'
                                               'time_kurtosis, time_skewness, amount_mean,'
                                               'amount_median, amount_std, amount_kurtosis,'
                                               'amount_skewness FROM ArrivedSessions '
                                               'WHERE type = -1')
        self.semaphore.release()

        return features
