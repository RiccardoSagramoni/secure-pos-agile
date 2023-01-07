import json
import logging

from utility.json_validation import validate_json_data_file


class Configuration:
    def __init__(self, json_configuration_path: str, json_schema_path: str):
        # Open configuration file
        with open(json_configuration_path, "r") as file:
            # Load JSON configuration
            json_conf = json.load(file)
            # Validate configuration
            if not validate_json_data_file(json_conf, json_schema_path):
                logging.error("Impossible to load the ingestion system "
                              "configuration: JSON file is not valid")
                raise ValueError("Ingestion System configuration failed")
            
            # Add JSON attributes to current object
            self.ip_address = json_conf['ip_address']
            self.port = int(json_conf['port'])
            self.database_path = json_conf['database_path']
            self.preparation_system_url = json_conf['preparation_system_url']
            self.monitoring_system_url = json_conf['monitoring_system_url']
            self.min_transactions_per_session = int(json_conf['min_transactions_per_session'])
            self.max_invalid_attributes_allowed = int(json_conf['max_invalid_attributes_allowed'])
            self.execution_window_length = int(json_conf['execution_window_length'])
            self.monitoring_window_length = int(json_conf['min_transactions_per_session'])
            self.is_development_mode = bool(json_conf['min_transactions_per_session'])
