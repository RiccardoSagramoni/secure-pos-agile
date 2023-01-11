import json
import logging
import os

import utility
from utility.json_validation import validate_json_data_file


class ExecutionConfiguration:
    def __init__(self, json_configuration_path: str, json_schema_path: str):
        # Open configuration file
        with open(os.path.join(utility.data_folder, json_configuration_path), "r", encoding="UTF-8") as file:
            # Load JSON configuration
            json_conf = json.load(file)
            # Validate configuration
            if not validate_json_data_file(json_conf, json_schema_path):
                logging.error("Impossible to load the execution system "
                              "configuration: JSON file is not valid")
                raise ValueError("Execution System configuration failed")

            # Add JSON attributes to current object
            self.system_ip = json_conf['system_ip']
            self.system_port = int(json_conf['system_port'])
            self.monitoring_system_url = json_conf['monitoring_system_url']
            self.execution_window_length = int(json_conf['execution_window_length'])
            self.monitoring_window_length = int(json_conf['monitoring_window_length'])
