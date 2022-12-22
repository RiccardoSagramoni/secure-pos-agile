import json
import os

from jsonschema import exceptions, validate
from utility import get_project_folder, get_json_schema_folder


def validate_json(json_data, schema) -> bool:
    """
    Validate a json object against a json schema.
    :param json_data: json object
    :param schema: json schema
    :return: True if json object is valid, False otherwise.
    """
    try:
        validate(instance=json_data, schema=schema)
    except exceptions.ValidationError:
        return False
    return True


def validate_json_data_file(json_data, schema_filename):
    """
    Validate a json object against a json schema in a file
    :param json_data: json object
    :param schema_filename: name of the file containing the json schema
    :return: True if json object is valid, False otherwise
    """
    schema_path = os.path.join(get_json_schema_folder(), schema_filename)

    with open(schema_path, "r", encoding="UTF-8") as file:
        json_schema = json.load(file)

    return validate_json(json_data, json_schema)


def validate_json_file_file(json_filename, schema_filename):
    """
    Validate a json file against a json schema in a file
    :param json_filename: file containing the json object
    :param schema_filename: file containing the json schema
    :return: True if json object is valid, False otherwise
    """
    json_path = os.path.join(get_project_folder(), json_filename)
    
    with open(json_path, "r", encoding="UTF-8") as file:
        return validate_json_data_file(json.load(file), schema_filename)
