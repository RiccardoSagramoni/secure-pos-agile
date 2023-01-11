import json

import numpy as np
from scipy.stats import skew, kurtosis

from data_objects.raw_session import RawSession
from preparation_system.prepared_session import PreparedSession


class PreparedSessionGenerator:

    def __init__(self, raw_session: RawSession):
        self.raw_session = raw_session
        self.prepared_session = None
        self.time_diff = None
        self.amount = []

    def generate_time_diff(self):
        transactions = self.raw_session.transactions
        time = []
        for transaction in transactions:
            # converto time (str) in long int
            hour, minute, sec = transaction.commercial.time.split(':')
            time_int = int(hour) * 3600 + int(minute) * 60 + int(sec)
            time.append(time_int)
        time.sort()
        time_array = np.array(time)
        self.time_diff = list(np.diff(time_array))

    @staticmethod
    def generate_mean(data_list):
        data_array = np.array(data_list)
        return np.mean(data_array)

    @staticmethod
    def generate_std(data_list):
        data_array = np.array(data_list)
        return np.std(data_array)

    @staticmethod
    def generate_skew(data_list):
        data_array = np.array(data_list)
        return skew(data_array)

    @staticmethod
    def generate_median(data_list):
        data_array = np.array(data_list)
        return np.median(data_array)

    @staticmethod
    def generate_kurtosis(data_list):
        data_array = np.array(data_list)
        return kurtosis(data_array)

    def get_amount(self):
        transactions = self.raw_session.transactions
        for transaction in transactions:
            self.amount.append(float(transaction.commercial.amount))

    def generate_prepared_session_json(self):
        prepared_session_dict = self.prepared_session.to_dict()
        with open("../../data/preparation_system/prepared_session.json",
                  'w', encoding="UTF-8") as json_file:
            json.dump(prepared_session_dict, json_file, indent=2)

    def extract_features(self):
        self.generate_time_diff()

        time_mean = self.generate_mean(self.time_diff)
        time_median = self.generate_median(self.time_diff)
        time_std = self.generate_std(self.time_diff)
        time_kurtosis = self.generate_kurtosis(self.time_diff)
        time_skew = self.generate_skew(self.time_diff)

        self.get_amount()
        amount_mean = self.generate_mean(self.amount)
        amount_median = self.generate_median(self.amount)
        amount_std = self.generate_std(self.amount)
        amount_kurtosis = self.generate_kurtosis(self.amount)
        amount_skew = self.generate_skew(self.amount)

        self.prepared_session = PreparedSession(self.raw_session.session_id, time_mean,
                                                time_std, time_skew, time_median,
                                                time_kurtosis, amount_mean, amount_median,
                                                amount_std, amount_kurtosis, amount_skew,
                                                self.raw_session.attack_risk_label)

        return self.prepared_session.to_dict()
