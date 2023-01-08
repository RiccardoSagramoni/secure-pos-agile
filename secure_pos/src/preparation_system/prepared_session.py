
class PreparedSession:

    def __init__(self, session_id, time_mean, time_std, time_skew,
                 amount_1, amount_2, amount_3, amount_4, amount_5,
                 amount_6, amount_7, amount_8, amount_9, amount_10,
                 label):
        self.session_id = session_id
        self.time_mean = time_mean
        self.time_std = time_std
        self.time_skew = time_skew
        self.amount_1 = amount_1
        self.amount_2 = amount_2
        self.amount_3 = amount_3
        self.amount_4 = amount_4
        self.amount_5 = amount_5
        self.amount_6 = amount_6
        self.amount_7 = amount_7
        self.amount_8 = amount_8
        self.amount_9 = amount_9
        self.amount_10 = amount_10
        self.label = label

    def to_dict(self):
        return {
            "id": [self.session_id],
            "time_mean": [self.time_mean],
            "time_std": [self.time_std],
            "time_skew": [self.time_skew],
            "amount_1": [self.amount_1],
            "amount_2": [self.amount_2],
            "amount_3": [self.amount_3],
            "amount_4": [self.amount_4],
            "amount_5": [self.amount_5],
            "amount_6": [self.amount_6],
            "amount_7": [self.amount_7],
            "amount_8": [self.amount_8],
            "amount_9": [self.amount_9],
            "amount_10": [self.amount_10],
            "type": [-1],
            "label": [self.label]
        }
