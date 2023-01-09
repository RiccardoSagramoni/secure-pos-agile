import re

from data_objects.record_data import CommercialData, GeoData, NetworkData


def validate_string_with_regex(string: str, regex: str) -> bool:
    """
    Validate a string against a given pattern expression.
    :param string: string to validate.
    :param regex: pattern expression (regex).
    :return: True if string matches the pattern, False otherwise.
    """
    if string is None or not isinstance(string, str):
        return False
    result = re.match(pattern=regex, string=string)
    return bool(result)


class CommercialDataValidator:
    
    def __init__(self, data: CommercialData):
        self.__commercial_data = data
    
    def validate_cardid(self) -> bool:
        return validate_string_with_regex(
            self.__commercial_data.cardid,
            "^\\w{8}-\\w{4}-\\w{4}-\\w{4}-\\w{12}$"
        )
    
    def validate_posid(self) -> bool:
        return validate_string_with_regex(
            self.__commercial_data.posid,
            "^\\w{8}-\\w{4}-\\w{4}-\\w{4}-\\w{12}$"
        )
    
    def validate_posname(self) -> bool:
        return validate_string_with_regex(
            self.__commercial_data.posname,
            "^[A-Za-z\\s\\.,.:\\-\"']+$"
        )
    
    def validate_date(self) -> bool:
        return validate_string_with_regex(
            self.__commercial_data.date,
            "^[0-9]{4}\\-[0-9]{1,2}\\-[0-9]{1,2}$"
        )
    
    def validate_time(self) -> bool:
        return validate_string_with_regex(
            self.__commercial_data.time,
            "^[0-9]{2}:[0-9]{2}:[0-9]{2}$"
        )
    
    def validate_payment_type(self) -> bool:
        return validate_string_with_regex(
            self.__commercial_data.payment_type,
            "^[A-Z]*$"
        )
    
    def validate_payment_circuit(self) -> bool:
        return validate_string_with_regex(
            self.__commercial_data.payment_circuit,
            "^[A-Z]*$"
        )
    
    def validate_amount(self) -> bool:
        return validate_string_with_regex(
            self.__commercial_data.payment_circuit,
            "^[0-9]+\\.[0-9]{2}$"
        )
    
    def validate_currency(self) -> bool:
        return validate_string_with_regex(
            self.__commercial_data.currency,
            "^[A-Z]*$"
        )
    
    def count_invalid_attributes(self) -> int:
        return int(
            (not self.validate_cardid())
            + (not self.validate_posid())
            + (not self.validate_posname())
            + (not self.validate_date())
            + (not self.validate_time())
            + (not self.validate_payment_type())
            + (not self.validate_payment_circuit())
            + (not self.validate_amount())
            + (not self.validate_currency())
        )


class GeoDataValidator:
    
    def __init__(self, data: GeoData):
        self.__geo_data = data
    
    def validate_loc_name(self) -> bool:
        return validate_string_with_regex(
            self.__geo_data.loc_name,
            "^[A-Z]{2}$"
        )
    
    def validate_p_id(self) -> bool:
        return validate_string_with_regex(
            self.__geo_data.p_id,
            "^\\w{8}-\\w{4}-\\w{4}-\\w{4}-\\w{12}$"
        )
    
    def validate_longitude(self) -> bool:
        return validate_string_with_regex(
            self.__geo_data.longitude,
            "^((\\-?|\\+?)?\\d+(\\.\\d+)?)$"
        )
    
    def validate_latitude(self) -> bool:
        return validate_string_with_regex(
            self.__geo_data.latitude,
            "^((\\-?|\\+?)?\\d+(\\.\\d+)?)$"
        )
    
    def count_invalid_attributes(self) -> int:
        return int(
            (not self.validate_loc_name())
            + (not self.validate_p_id())
            + (not self.validate_longitude())
            + (not self.validate_latitude())
        )


class NetworkDataValidator:
    
    def __init__(self, data: NetworkData):
        self.__network_data = data
    
    def validate_ip(self) -> bool:
        return validate_string_with_regex(
            self.__network_data.ip,
            "^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.){3}"
            "(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$"
        )
    
    def count_invalid_attributes(self) -> int:
        return int(
            not self.validate_ip()
        )
