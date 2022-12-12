import pytest

from utility.json import validate_json
from geographical_json import geographical_schema, geographical_good_json, geographical_bad_json


@pytest.mark.parametrize('data', geographical_good_json)
def test_validate_geographical_correct_json(data):
    assert validate_json(data, geographical_schema)


@pytest.mark.parametrize('data', geographical_bad_json)
def test_validate_geographical_wrong_json(data):
    assert not validate_json(data, geographical_schema)
