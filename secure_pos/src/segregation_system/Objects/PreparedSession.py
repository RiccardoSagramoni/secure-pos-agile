class PreparedSession:

    def __init__(self, features, label):
        self.time_mean = features[0]
        self.time_median = features[1]
        self.time_std = features[2]
        self.time_kurtosis = features[3]
        self.time_skewness = features[4]
        self.amount_mean = features[5]
        self.amount_median = features[6]
        self.amount_std = features[7]
        self.amount_kurtosis = features[8]
        self.amount_skewness = features[9]
        self.label = label

    def get_features(self) -> object:
        """
        Function that extracts the features of a specific session
        :return: Array with 13 fields, one for each feature
        """
        array = [self.time_mean, self.time_median, self.time_std,
                 self.time_kurtosis, self.time_skewness, self.amount_mean,
                 self.amount_median, self.amount_std, self.amount_kurtosis,
                 self.amount_skewness]
        return array

    def get_label(self):
        """
        Function that extracts the label of a specific session
        :return: integer representing the label
        """
        return [self.label]
