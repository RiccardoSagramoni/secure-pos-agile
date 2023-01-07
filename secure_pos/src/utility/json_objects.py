from typing import Any

from utility.json_validation import validate_json_data_file


def load_json_in_object(obj: Any, json_data: dict, json_schema_path: str) -> None:
    # Validate configuration
    if not validate_json_data_file(json_data, json_schema_path):
        raise ValueError()
    # Add JSON attributes to current object
    obj.__dict__.update(json_data)
