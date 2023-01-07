import pandas


class CommercialData:
    def __init__(self, transaction_data: pandas.Series):
        self.event_id = transaction_data.event_id
        self.cardid = transaction_data.cardid
        self.posid = transaction_data.posid
        self.posname = transaction_data.posname
        self.date = transaction_data.date
        self.time = transaction_data.time
        self.payment_type = transaction_data.payment_type
        self.payment_circuit = transaction_data.payment_circuit
        self.amount = transaction_data.amount
        self.currency = transaction_data.currency


class NetworkData:
    def __init__(self, transaction_data: pandas.Series):
        self.event_id = transaction_data.event_id
        self.ip = transaction_data.ip


class GeoData:
    def __init__(self, transaction_data: pandas.Series):
        self.event_id = transaction_data.event_id
        self.loc_name = transaction_data.loc_name
        self.p_id = transaction_data.p_id
        self.longitude = transaction_data.longitude
        self.latitude = transaction_data.latitude
