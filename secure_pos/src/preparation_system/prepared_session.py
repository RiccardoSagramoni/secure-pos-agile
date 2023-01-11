class PreparedSession:

    def __init__(self, session_id, time_mean, time_std, time_skew,
                 time_median, time_kurtosis, amount_mean, amount_median,
                 amount_std, amount_kurtosis, amount_skew, label):
        self.session_id = session_id
        self.time_mean = time_mean
        self.time_median = time_median
        self.time_std = time_std
        self.time_kurtosis = time_kurtosis
        self.time_skew = time_skew
        self.amount_mean = amount_mean
        self.amount_median = amount_median
        self.amount_std = amount_std
        self.amount_kurtosis = amount_kurtosis
        self.amount_skew = amount_skew
        self.label = label

    def to_dict(self):
        return {
            "id": [self.session_id],
            "time_mean": [float(self.time_mean)],
            "time_median": [float(self.time_median)],
            "time_std": [float(self.time_std)],
            "time_kurtosis": [float(self.time_kurtosis)],
            "time_skew": [float(self.time_skew)],
            "amount_mean": [float(self.amount_mean)],
            "amount_median": [float(self.amount_median)],
            "amount_std": [float(self.amount_std)],
            "amount_kurtosis": [float(self.amount_kurtosis)],
            "amount_skew": [float(self.amount_skew)],
            "type": [-1],
            "label": [self.label]
        }
