from data_objects.transaction import Transaction
from ingestion_system.configuration import Configuration
from validation.record_data_validator \
    import CommercialDataValidator, GeoDataValidator, NetworkDataValidator


class TransactionValidator:
    
    def __init__(self, transaction: Transaction, conf: Configuration):
        self.__transaction = transaction
        self.__max_invalid_attributes_allowed = conf.max_invalid_attributes_allowed
    
    def is_valid(self) -> bool:
        invalid_attributes_num = (
                CommercialDataValidator(self.__transaction.commercial).count_invalid_attributes()
                + GeoDataValidator(self.__transaction.geo).count_invalid_attributes()
                + NetworkDataValidator(self.__transaction.network).count_invalid_attributes()
        )
        return invalid_attributes_num <= self.__max_invalid_attributes_allowed
