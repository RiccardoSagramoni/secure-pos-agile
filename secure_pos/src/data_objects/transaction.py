import pandas

from data_objects.record_data import CommercialData, GeoData, NetworkData
from ingestion_system.configuration import Configuration
from validation.record_data_validator import CommercialDataValidator, GeoDataValidator, NetworkDataValidator


class Transaction:
    
    def __init__(self, data: pandas.Series, conf: Configuration):
        self.commercial = CommercialData(data)
        self.geo = GeoData(data)
        self.network = NetworkData(data)
        self.configuration = conf
    
    def is_valid(self) -> bool:
        invalid_attributes_num = (
            CommercialDataValidator(self.commercial).detect_invalid_attributes()
            + GeoDataValidator(self.geo).detect_invalid_attributes()
            + NetworkDataValidator(self.network).detect_invalid_attributes()
        )
        return invalid_attributes_num <= self.configuration.max_invalid_attributes_allowed
    