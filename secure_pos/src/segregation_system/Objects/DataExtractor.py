import pandas as pd

from segregation_system.Objects.CollectedSessions import CollectedSessions
from src.database.DBManager import DBManager


class DataExtractor:
    """
    Class that manages the connection with the DB in order to extract
    the required data and return it to the front-end
    """

    def __init__(self, path_db, semaphore):
        self.database = DBManager(path_db)
        # Paying attention to critical runs
        semaphore.acquire()
        # Extracts data
        features = self.database.read_sql('SELECT time_mean, time_std, time_skew,'
                                          'amount_1, amount_2, amount_3, amount_4, amount_5,'
                                          'amount_6, amount_7, amount_8, amount_9, amount_10 '
                                          'FROM ArrivedSessions WHERE type = -1')
        # Extracts labels for current data
        labels = self.database.read_sql('SELECT label FROM ArrivedSessions WHERE type = -1')
        semaphore.release()

        self.current_sessions = CollectedSessions(features, labels)

    def count_labels(self):
        """
        Extracts the amount of 'Attack' and 'Normal' labels
        in the unallocated records present inside the DB
        :return: numPy array: [#_0, #_1]
        """
        labels = self.current_sessions.get_labels()
        count_normal = 0
        count_attack = 0

        for i in range(len(labels)):
            if labels['label'][i] == 'NORMAL':
                count_normal += 1
            else:
                count_attack += 1

        return [count_normal, count_attack]

    def extract_features(self) -> object:
        """
        Function that performs a query that extract the data
        needed to plot the radar diagram in order to evaluate
        the data quality
        :return: Dataframe
        """
        data = self.current_sessions.get_features()
        # Extract all the unallocated data
        data_frame = pd.DataFrame(data,
                                  columns=['time_mean', 'time_std', 'time_skew', 'amount_1', 'amount_2',
                                           'amount_3', 'amount_4', 'amount_5', 'amount_6', 'amount_7', 'amount_8',
                                           'amount_9', 'amount_10'])

        return data_frame

    def extract_labels(self):

        data = self.current_sessions.get_labels()
        data_frame = pd.DataFrame(data,
                                  columns=['label'])

        return data_frame
