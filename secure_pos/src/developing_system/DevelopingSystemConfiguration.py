import json
import logging
import os

import utility
from utility.json_validation import validate_json_data_file

class DevelopingSystemConfiguration:

    def __init__(self, json_development_system_configuration_path: str, json_schema_path: str):

        # Open configuration file
        with open(os.path.join(utility.data_folder, json_development_system_configuration_path), "r", encoding="UTF-8") as file:
            # Load JSON configuration
            json_development_system_conf = json.load(file)
            # Validate configuration
            if not validate_json_data_file(json_development_system_conf, json_schema_path):
                logging.error("Impossible to load the development system "
                              "configuration: JSON file is not valid")
                raise ValueError("Development System configuration failed")

            # Add JSON attributes to current object
            self.ip_address = json_development_system_conf['ip_address']
            self.port = int(json_development_system_conf['port'])
            self.execution_system_url = json_development_system_conf['execution_system_url']
            self.is_testing_phase = json_development_system_conf['is_testing_phase']