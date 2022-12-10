import jsonschema


def validate_json(json_data, schema) -> bool:
    """
    Validate a json object against a json schema.
    :param json_data: json object
    :param schema: json schema
    :return: True if json object is valid, False otherwise.
    """
    try:
        jsonschema.validate(instance=json_data, schema=schema)
    except jsonschema.exceptions.ValidationError:
        return False
    return True
