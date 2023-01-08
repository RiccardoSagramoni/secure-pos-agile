from data_objects.record_data import CommercialData, GeoData, NetworkData


class Transaction:
    def __init__(self, commercial: CommercialData, geo: GeoData, network: NetworkData):
        self.commercial = commercial
        self.geo = geo
        self.network = network
