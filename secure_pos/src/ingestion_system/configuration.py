import json
import logging

from utility.json_validation import validate_json_data_file


class Configuration:

    def __init__(self, json_configuration_path: str, json_schema_path: str):
        # Open configuration file
        self.max_invalid_attributes_allowed = None
        self.test = None
        with open(json_configuration_path, "r") as file:
            # Load JSON configuration
            json_configuration = json.load(file)
            # Validate configuration
            if not validate_json_data_file(json_configuration, json_schema_path):
                logging.error("Impossible to load the ingestion system "
                              "configuration: JSON file is not valid")
                raise ValueError("Ingestion System configuration failed")
            # Add JSON attributes to current object
            self.__dict__.update(json_configuration)
