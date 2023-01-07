import pandas

from data_objects.record_data import CommercialData, GeoData, NetworkData


class Transaction:
    
    def __init__(self, data: pandas.Series):
        self.commercial = CommercialData(data)
        self.geo = GeoData(data)
        self.network = NetworkData(data)
