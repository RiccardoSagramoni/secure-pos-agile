geographical_schema = {
    "$id": "https://example.com/geographical-location.schema.json",
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "Longitude and Latitude Values",
    "description": "A geographical coordinate.",
    "required": ["latitude", "longitude"],
    "type": "object",
    "properties": {
        "latitude": {
            "type": "number",
            "minimum": -90,
            "maximum": 90
        },
        "longitude": {
            "type": "number",
            "minimum": -180,
            "maximum": 180
        }
    }
}


geographical_good_json = [
    {
        "latitude": 48.858093,
        "longitude": 2.294694
    },
    {
        "latitude": 0,
        "longitude": 0
    },
    {
        "latitude": 12.567,
        "longitude": -3.23
    },
    {
        "latitude": 90,
        "longitude": -180
    }
]

geographical_bad_json = [
    {
        "latitude": "wrong",
        "longitude": 2.294694
    },
    {
        "latitude": 120,
        "longitude": 0
    },
    {
        "latitude": 0,
        "longitude": "f"
    },
    {
        "latitude": -10,
        "longitude": 1000.123
    }
]
