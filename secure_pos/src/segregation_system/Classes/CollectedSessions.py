import pandas as pd
from segregation_system.Classes.PreparedSession import PreparedSession


class CollectedSessions:
    """
    Class representing the collection of sessions we are currently working on
    """
    def __init__(self, features, labels):
        self.prep_sessions = []
        self.sessions_count = 0

        for i in range(len(features)):
            p_s = PreparedSession(features.values[i, :], labels.values[i])
            self.prep_sessions.append(p_s)
            self.sessions_count += 1

        self.get_features()

    def get_features(self):
        """
        Extracts a list of features we are currently working on: [[...features...],[...features...],...]
        :return: list of the list of features
        """
        features = []

        for i in range(self.sessions_count):
            feature = self.prep_sessions[i].get_features()
            features.append(feature)

        return features

    def get_labels(self):
        """
        Function that extract a lis tof labels: [[label],[label], ... ]
        :return: data frame
        """
        labels = pd.DataFrame(columns=['label'])

        for i in range(self.sessions_count):
            label = self.prep_sessions[i].get_label()
            labels.loc[i] = label[0][0]

        return labels

    def count_labels(self):
        """
        Count the number of Normal and Attack labels inside the currently used data
        :return: list of counted labels: [#_0, #_1]
        """
        labels = self.get_labels()
        count_0 = 0
        count_1 = 0

        for i in range(self.sessions_count):
            if labels[i][0] == 0:
                count_0 += 1
            else:
                count_1 += 1

        return [count_0, count_1]
