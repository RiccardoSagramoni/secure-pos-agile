import pandas as pd

from segregation_system.Objects.CollectedSessions import CollectedSessions


class DataExtractor:
    """
    Class that manages the connection with the DB in order to extract
    the required data and return it to the front-end
    """

    def __init__(self, db_handler):

        [features, labels] = db_handler.extract_all_unallocated_data()

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
                                  columns=['time_mean', 'time_median', 'time_std',
                                           'time_kurtosis', 'time_skewness', 'amount_mean',
                                           'amount_median', 'amount_std', 'amount_kurtosis',
                                           'amount_skewness'])

        return data_frame

    def extract_labels(self):

        data = self.current_sessions.get_labels()
        data_frame = pd.DataFrame(data,
                                  columns=['label'])

        return data_frame

