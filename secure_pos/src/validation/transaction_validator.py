from data_objects.transaction import Transaction
from ingestion_system.configuration import Configuration
from validation.record_data_validator import CommercialDataValidator, GeoDataValidator, NetworkDataValidator


class TransactionValidator:
    
    def __init__(self, transaction: Transaction, conf: Configuration):
        self.transaction = transaction
        self.configuration = conf
    
    def is_valid(self) -> bool:
        invalid_attributes_num = (
                CommercialDataValidator(self.transaction.commercial).count_invalid_attributes()
                + GeoDataValidator(self.transaction.geo).count_invalid_attributes()
                + NetworkDataValidator(self.transaction.network).count_invalid_attributes()
        )
        return invalid_attributes_num <= self.configuration.max_invalid_attributes_allowed
