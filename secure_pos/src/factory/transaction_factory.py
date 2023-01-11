import pandas

from data_objects.transaction import Transaction
from factory.record_data_factory import CommercialDataFactory, GeoDataFactory, NetworkDataFactory


class TransactionFactory:
    """
    Factory responsible for generating Transaction objects.
    """
    
    @staticmethod
    def generate_from_json_dict(data: dict) -> Transaction:
        return Transaction(
            commercial=CommercialDataFactory.generate_from_json_dict(data['commercial']),
            geo=GeoDataFactory.generate_from_json_dict(data['geo']),
            network=NetworkDataFactory.generate_from_json_dict(data['network'])
        )
    
    @staticmethod
    def generate_from_series(data: pandas.Series) -> Transaction:
        return Transaction(
            commercial=CommercialDataFactory.generate_from_series(data),
            geo=GeoDataFactory.generate_from_series(data),
            network=NetworkDataFactory.generate_from_series(data)
        )
