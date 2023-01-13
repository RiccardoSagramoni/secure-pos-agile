import pandas as pd
from segregation_system.Objects.PreparedSession import PreparedSession


class CollectedSessions:
    """
    Class representing the collection of sessions we are currently working on
    """
    def __init__(self, data, labels):
        self.prep_sessions = []
        self.sessions_count = 0

        for i in range(len(data)):
            p_s = PreparedSession(data.values[i, :], labels.values[i])
            self.prep_sessions.append(p_s)
            self.sessions_count += 1

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

    def get_all(self):
        """
        Extracts a list of features we are currently working on: [[...features...],[...features...],...]
        :return: list of the list of features
        """
        data = []

        for i in range(self.sessions_count):
            _all = self.prep_sessions[i].get_all()
            data.append(_all)

        return data