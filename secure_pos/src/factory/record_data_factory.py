import pandas

from data_objects.record_data import CommercialData, NetworkData, GeoData


class CommercialDataFactory:
    """
    Factory responsible for generating CommercialData objects.
    """
    
    @staticmethod
    def generate_from_json_dict(data: dict) -> CommercialData:
        return CommercialData(
            data['event_id'],
            data['cardid'],
            data['posid'],
            data['posname'],
            data['date'],
            data['time'],
            data['payment_type'],
            data['payment_circuit'],
            data['amount'],
            data['currency']
        )
    
    @staticmethod
    def generate_from_series(transaction_data: pandas.Series) -> CommercialData:
        return CommercialData(
            transaction_data.event_id,
            transaction_data.cardid,
            transaction_data.posid,
            transaction_data.posname,
            transaction_data.date,
            transaction_data.time,
            transaction_data.payment_type,
            transaction_data.payment_circuit,
            transaction_data.amount,
            transaction_data.currency
        )


class NetworkDataFactory:
    """
    Factory responsible for generating NetworkData objects.
    """
    
    @staticmethod
    def generate_from_json_dict(data: dict) -> NetworkData:
        return NetworkData(
            data['event_id'],
            data['ip']
        )
    
    @staticmethod
    def generate_from_series(transaction_data: pandas.Series) -> NetworkData:
        return NetworkData(
            transaction_data.event_id,
            transaction_data.ip
        )


class GeoDataFactory:
    """
    Factory responsible for generating GeoData objects.
    """
    
    @staticmethod
    def generate_from_json_dict(data: dict) -> GeoData:
        return GeoData(
            data['event_id'],
            data['loc_name'],
            data['p_id'],
            data['longitude'],
            data['latitude']
        )
    
    @staticmethod
    def generate_from_series(transaction_data: pandas.Series) -> GeoData:
        return GeoData(
            transaction_data.event_id,
            transaction_data.loc_name,
            transaction_data.p_id,
            transaction_data.longitude,
            transaction_data.latitude
        )
