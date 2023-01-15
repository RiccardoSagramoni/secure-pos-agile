import json
import logging
import os

import utility
from utility.json_validation import validate_json_data_file

CONFIGURATION_PATH = 'segregation_system/segregation_configuration.json'
CONFIGURATION_SCHEMA_PATH = './json_schema/segregation_configuration_schema.json'


class SegregationSystemConfiguration:
    """
    Object needed to store contained inside the config file
    """
    def __init__(self):
        # Open configuration file
        with open(os.path.join(utility.data_folder, CONFIGURATION_PATH), "r", encoding="UTF-8") as file:
            # Load JSON configuration
            json_conf = json.load(file)
            # Validate configuration
            if not validate_json_data_file(json_conf, CONFIGURATION_SCHEMA_PATH):
                logging.error("Impossible to load the segregation system "
                              "configuration: JSON file is not valid")
                raise ValueError("Segregation System configuration failed")

            # Add JSON attributes to current object
            self.development_system_url = json_conf['development_system_url']
            self.session_nr_threshold = int(json_conf['session_nr_threshold'])
            self.development_mode = json_conf['development_mode']
