from src.database.DBManager import DBManager


class DataStatsExtractor:
    """
    Class that manages the connection with the DB in order to extract
    the required data and return it to the front-end
    """

    def __init__(self, path_db):
        self.database = DBManager(path_db)

    def count_labels(self):
        """
        Extracts the amount of 'Attack' and 'Normal' labels
        in the unallocated records present inside the DB
        :return: Dataframe
        """
        # Count the number of unallocated records
        # that have 'Attack' as label
        df_lab1 = self.database.read_sql(
            'SELECT COUNT(*) FROM ArrivedSessions WHERE type = -1 AND label = 0')

        # Count the number of unallocated records
        # that have 'Normal' as label
        df_lab2 = self.database.read_sql(
            'SELECT COUNT(*) FROM ArrivedSessions WHERE type = -1 AND label = 1')

        data = [df_lab1, df_lab2]
        return data

    def extract_radar_diagram_data(self):
        """
        Function that performs a query that extract the data
        needed to plot the radar diagram in order to evaluate
        the data quality
        :return: Dataframe
        """
        # Extract all the unallocated data
        data_frame = self.database.read_sql('SELECT time_mean, time_skew, time_std, '
                                            'amount_1, amount_2, amount_3, amount_4, amount_5,'
                                            'amount_6, amount_7, amount_8, amount_9, amount_10,'
                                            'FROM ArrivedSessions WHERE type = -1')
        return data_frame
