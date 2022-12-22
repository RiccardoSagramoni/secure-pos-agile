import os
import json

from conftest import RECEIVE_JSON_URL, GET_JSON_URL, GET_JSON_DIR_URL, RECEIVE_API_JSON_FILENAME
from utility import get_project_folder


def test_get_json__get(client):
    response = client.get(GET_JSON_URL)
    assert response.status_code == 200


def test_get_json_inside_directory__get(client):
    response = client.get(GET_JSON_DIR_URL + '/example_dir.json')
    assert response.status_code == 200


def test_get_json_inside_directory__wrong_json_file(client):
    response = client.get(GET_JSON_DIR_URL + '/wrong.file')
    assert response.status_code == 404


def test_receive_json__post(client):

    destination_path = os.path.join(get_project_folder(), RECEIVE_API_JSON_FILENAME)
    content = {"result": "test passed"}
    response = client.post(RECEIVE_JSON_URL, json=content)
    assert response.status_code == 201

    # Check if received file is the same
    with open(destination_path, "r") as json_received_file:
        json_data = json.load(json_received_file)
        assert json_data == content

    # remove generate json file
    os.remove(destination_path)


def test_receive_json__wrong_validation_post(client):

    content = {"test": "validation error passed"}
    response = client.post(RECEIVE_JSON_URL, json=content)
    assert response.status_code == 400
