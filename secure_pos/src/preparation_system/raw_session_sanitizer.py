from statistics import mean

from data_objects.raw_session import RawSession
from validation.record_data_validator import CommercialDataValidator


class RawSessionSanitizer:

    def __init__(self, raw_session: RawSession, min_amount, max_amount):
        self.raw_session = raw_session
        self.min_amount = min_amount
        self.max_amount = max_amount

    def correct_outliers(self):
        transactions = self.raw_session.transactions
        for transaction in transactions:
            amount = float(transaction.commercial.amount)
            if amount < self.min_amount:
                transaction.commercial.amount = str(self.min_amount)
            if amount > self.max_amount:
                transaction.commercial.amount = str(self.max_amount)

    def correct_missing_time(self):
        transactions = self.raw_session.transactions
        time = []
        for transaction in transactions:
            time_str = transaction.commercial.time
            commercial_validator = CommercialDataValidator(transaction.commercial)
            res = commercial_validator.validate_time()
            if not res:
                continue
            hour, minute, sec = time_str.split(':')
            time_int = int(hour) * 3600 + int(minute) * 60 + int(sec)
            time.append(time_int)
        time_mean = int(mean(time))
        minute = time_mean // 60
        hour = minute // 60
        time_mean_str = "%02d:%02d:%02d" % (hour, minute % 60, time_mean % 60)
        for transaction in transactions:
            commercial_validator = CommercialDataValidator(transaction.commercial)
            res = commercial_validator.validate_time()
            if not res:
                transaction.commercial.time = time_mean_str

    def correct_missing_amount(self):
        transactions = self.raw_session.transactions
        amount = []
        for transaction in transactions:
            amount_str = transaction.commercial.amount
            commercial_validator = CommercialDataValidator(transaction.commercial)
            res = commercial_validator.validate_amount()
            if not res:
                continue
            amount.append(float(amount_str))
        amount_mean = mean(amount)
        for transaction in transactions:
            commercial_validator = CommercialDataValidator(transaction.commercial)
            res = commercial_validator.validate_amount()
            if not res:
                transaction.commercial.amount = str(amount_mean)
