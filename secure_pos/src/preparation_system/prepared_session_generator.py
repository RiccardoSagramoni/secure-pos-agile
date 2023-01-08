from statistics import mean, stdev

import numpy as np
from scipy.stats import skew

from data_objects.raw_session import RawSession
from preparation_system.prepared_session import PreparedSession


class PreparedSessionGenerator:

    def __init__(self, raw_session: RawSession):
        self.raw_session = raw_session
        self.preparedSession = None
        self.time_diff = []

    def generate_prepared_session_json(self):
        pass

    def generate_time_diff(self):
        pass

    def generate_time_mean(self):
        return mean(self.time_diff)

    def generate_time_std(self):
        return stdev(self.time_diff)

    def generate_time_skew(self):
        return skew(np.array(self.time_diff))

    def extract_features(self):
        self.generate_time_diff()
        time_mean = self.generate_time_mean()
        time_std = self.generate_time_std()
        time_skew = self.generate_time_skew()

        self.preparedSession = PreparedSession(self.raw_session.session_id,
                                               time_mean,
                                               time_std,
                                               time_skew,
                                               ...,
                                               self.raw_session.attack_risk_label)

        return self.preparedSession.to_dict()
