class PreparedSession:

    def __init__(self, features, label):
        self.time_mean = features[0]
        self.time_std = features[1]
        self.time_skew = features[2]
        self.amount_1 = features[3]
        self.amount_2 = features[4]
        self.amount_3 = features[5]
        self.amount_4 = features[6]
        self.amount_5 = features[7]
        self.amount_6 = features[8]
        self.amount_7 = features[9]
        self.amount_8 = features[10]
        self.amount_9 = features[11]
        self.amount_10 = features[12]
        self.label = label

    def get_features(self) -> object:
        """
        Function that extracts the features of a specific session
        :return: Array with 13 fields, one for each feature
        """
        array = [self.time_mean, self.time_std, self.time_skew,
                 self.amount_1, self.amount_2, self.amount_3,
                 self.amount_4, self.amount_5, self.amount_6,
                 self.amount_7, self.amount_8, self.amount_9,
                 self.amount_10]
        return array

    def get_label(self):
        """
        Function that extracts the label of a specific session
        :return: integer representing the label
        """
        return [self.label]
