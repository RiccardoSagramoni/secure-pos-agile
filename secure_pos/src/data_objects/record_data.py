class CommercialData:
    def __init__(self, event_id: str, cardid: str, posid: str, posname: str,
                 date: str, time: str, payment_type: str, payment_circuit: str,
                 amount: str, currency: str):
        self.event_id = event_id
        self.cardid = cardid
        self.posid = posid
        self.posname = posname
        self.date = date
        self.time = time
        self.payment_type = payment_type
        self.payment_circuit = payment_circuit
        self.amount = amount
        self.currency = currency


class NetworkData:
    def __init__(self, event_id: str, ip: str):
        self.event_id = event_id
        self.ip = ip


class GeoData:
    def __init__(self, event_id: str, loc_name: str, p_id: str,
                 longitude: str, latitude: str):
        self.event_id = event_id
        self.loc_name = loc_name
        self.p_id = p_id
        self.longitude = longitude
        self.latitude = latitude
