import json
import os
import logging

from utility.json_validation import validate_json_data_file

RESPONSE_SCHEMA = 'segregation_response_schema.json'


def extract_json_response(file) -> object:
    """
    Function that extract the Data Analyst response from the file
    :param file: path of the file to be checked
    :return: string containing the response
    """
    if os.path.exists(file):
        with open(file, 'r+', encoding='utf-8') as file_opened:
            data = json.load(file_opened)
            # Validate configuration
            if not validate_json_data_file(file, RESPONSE_SCHEMA):
                logging.error("Impossible to load the segregation system "
                              "configuration: JSON file is not valid")
                raise ValueError("Segregation System configuration failed")
            result = data.pop('response')
            # TODO Remove comments
            # data['response'] = 'None'

            # Rewind needed for overwriting and reset the variable
            # file_opened.seek(0)
            # json.dump(data, file_opened)
            # file_opened.truncate()
    return result

