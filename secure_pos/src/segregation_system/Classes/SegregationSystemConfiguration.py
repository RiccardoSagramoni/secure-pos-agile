import json
import logging

from utility.json_validation import validate_json_data_file


class SegregationSystemConfiguration:
    def __init__(self, json_configuration_path: str, json_schema_path: str):
        # Open configuration file
        print()
        with open(json_configuration_path, "r", encoding="UTF-8") as file:
            # Load JSON configuration
            json_conf = json.load(file)
            # Validate configuration
            if not validate_json_data_file(json_conf, json_schema_path):
                logging.error("Impossible to load the segregation system "
                              "configuration: JSON file is not valid")
                raise ValueError("Segregation System configuration failed")

            # Add JSON attributes to current object
            self.development_system_ip = json_conf['development_system']['ip']
            self.development_system_port = int(json_conf['development_system']['port'])
            self.session_nr_threshold = int(json_conf['session_nr_threshold'])
            self.development_mode = json_conf['development_mode']

