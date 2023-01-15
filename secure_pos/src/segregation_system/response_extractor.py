import json
import os
import logging

import utility
from utility.json_validation import validate_json_data_file


class ResponseExtractor:
    """
    Class that extracts the data Analyst response from a JSON file
    """

    def __init__(self):
        self.schema_path = './json_schema/segregation_response_schema.json'
        self.data_balancing_response_path = 'segregation_system/responses/balancing_response.json'
        self.data_quality_response_path = 'segregation_system/responses/quality_response.json'

    def extract_json_response_balancing(self) -> object:
        """
        Function that extract the Data Analyst response from the file
        :return: string containing the response
        """
        if os.path.exists(os.path.join(utility.data_folder, self.data_balancing_response_path)):
            with open(os.path.join(utility.data_folder, self.data_balancing_response_path),
                      'r+',
                      encoding='utf-8') as file_opened:

                data = json.load(file_opened)
                # Validate configuration
                if not validate_json_data_file(dict(file_opened), self.schema_path):
                    logging.error("Impossible to load the segregation system "
                                  "configuration: JSON file is not valid")
                    raise ValueError("Segregation System configuration failed")
                result = data.pop('response')

                data['response'] = 'None'

                # Rewind needed for overwriting and reset the variable
                file_opened.seek(0)
                json.dump(data, file_opened)
                file_opened.truncate()
                return result

    def extract_json_response_quality(self) -> object:
        """
        Function that extract the Data Analyst response from the file
        :return: string containing the response
        """
        if os.path.exists(os.path.join(utility.data_folder, self.data_quality_response_path)):
            with open(os.path.join(utility.data_folder, self.data_quality_response_path),
                      'r+',
                      encoding='utf-8') as file_opened:

                data = json.load(file_opened)
                # Validate configuration
                if not validate_json_data_file(dict(file_opened), self.schema_path):
                    logging.error("Impossible to load the segregation system "
                                  "configuration: JSON file is not valid")
                    raise ValueError("Segregation System configuration failed")
                result = data.pop('response')

                data['response'] = 'None'

                # Rewind needed for overwriting and reset the variable
                file_opened.seek(0)
                json.dump(data, file_opened)
                file_opened.truncate()
                return result
