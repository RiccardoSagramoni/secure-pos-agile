import json

import numpy as np
from scipy.stats import skew, kurtosis

from data_objects.attack_risk_label import AttackRiskLabel
from data_objects.raw_session import RawSession
from preparation_system.prepared_session import PreparedSession


class PreparedSessionGenerator:

    def __init__(self, raw_session: RawSession):
        self.raw_session = raw_session
        self.prepared_session = None
        self.time_diff = None
        self.amount = []
        self.time_mean_max = 9525.56
        self.time_mean_min = 4119.33
        self.time_median_max = 10764
        self.time_median_min = 1593
        self.time_std_max = 13654.23
        self.time_std_min = 1927.56
        self.time_kurt_min = -1.69
        self.time_kurt_max = 3.65
        self.time_skew_min = -0.63
        self.time_skew_max = 2.31
        self.amount_mean_max = 801.65
        self.amount_mean_min = 292.56
        self.amount_median_min = 171.05
        self.amount_median_max = 851.55
        self.amount_std_min = 79.05
        self.amount_std_max = 339.44
        self.amount_kurt_min = -1.77
        self.amount_kurt_max = 2.29
        self.amount_skew_min = -1.4
        self.amount_skew_max = 1.78

    @staticmethod
    def normalize(value, value_min, value_max):
        if value < value_min:
            value = value_min
        elif value > value_max:
            value = value_max
        value_norm = (value - value_min) / (value_max - value_min)
        return value_norm

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

    def generate_mean(self, data_list, value_min, value_max):
        data_array = np.array(data_list)
        value = np.mean(data_array)
        value_norm = self.normalize(value, value_min, value_max)
        return value_norm

    def generate_std(self, data_list, value_min, value_max):
        data_array = np.array(data_list)
        value = np.std(data_array)
        value_norm = self.normalize(value, value_min, value_max)
        return value_norm

    def generate_skew(self, data_list, value_min, value_max):
        data_array = np.array(data_list)
        value = skew(data_array)
        value_norm = self.normalize(value, value_min, value_max)
        return value_norm

    def generate_median(self, data_list, value_min, value_max):
        data_array = np.array(data_list)
        value = np.median(data_array)
        value_norm = self.normalize(value, value_min, value_max)
        return value_norm

    def generate_kurtosis(self, data_list, value_min, value_max):
        data_array = np.array(data_list)
        value = kurtosis(data_array)
        value_norm = self.normalize(value, value_min, value_max)
        return value_norm

    def get_amount(self):
        transactions = self.raw_session.transactions
        for transaction in transactions:
            self.amount.append(float(transaction.commercial.amount))

    def generate_prepared_session_json(self):
        prepared_session_dict = self.prepared_session.to_dict()
        with open("../../data/preparation_system/prepared_session.json",
                  'w', encoding="UTF-8") as json_file:
            json.dump(prepared_session_dict, json_file, indent=2)

    def generate_label_class(self):
        if self.raw_session.attack_risk_label == AttackRiskLabel.ATTACK:
            label_class = 1
        else:
            label_class = 0
        return label_class

    def extract_features(self):
        self.generate_time_diff()

        time_mean = self.generate_mean(self.time_diff,
                                       self.time_mean_min, self.time_mean_max)
        time_median = self.generate_median(self.time_diff,
                                           self.time_median_min, self.time_median_max)
        time_std = self.generate_std(self.time_diff,
                                     self.time_std_min, self.time_std_max)
        time_kurtosis = self.generate_kurtosis(self.time_diff,
                                               self.time_kurt_min, self.time_kurt_max)
        time_skew = self.generate_skew(self.time_diff,
                                       self.time_skew_min, self.time_skew_max)

        self.get_amount()
        amount_mean = self.generate_mean(self.amount,
                                         self.amount_mean_min, self.amount_mean_max)
        amount_median = self.generate_median(self.amount,
                                             self.amount_median_min, self.amount_median_max)
        amount_std = self.generate_std(self.amount,
                                       self.amount_std_min, self.amount_std_max)
        amount_kurtosis = self.generate_kurtosis(self.amount,
                                                 self.amount_kurt_min, self.amount_kurt_max)
        amount_skew = self.generate_skew(self.amount,
                                         self.amount_skew_min, self.amount_skew_max)

        label_class = self.generate_label_class()

        self.prepared_session = PreparedSession(self.raw_session.session_id, time_mean,
                                                time_std, time_skew, time_median,
                                                time_kurtosis, amount_mean, amount_median,
                                                amount_std, amount_kurtosis, amount_skew,
                                                label_class)

        return self.prepared_session.to_dict()
