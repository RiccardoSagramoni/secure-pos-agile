import os

from fixture_app import *
from utility import get_project_folder, get_tests_folder


def test_get_file__get(client):
    response = client.get(GETFILE_URL)
    assert response.status_code == 200


def test_get_file_inside_directory__get(client):
    response = client.get(GETFILE_DIR_URL + '/label.csv')
    assert response.status_code == 200


def test_get_file_inside_directory__wrong_file(client):
    response = client.get(GETFILE_DIR_URL + '/wrong.file')
    assert response.status_code == 404


def test_receive_file__post(client):
    # Variables
    source_filename = "send.txt"
    source_path = os.path.join(get_tests_folder(), source_filename)
    dest_path = os.path.join(get_project_folder(), RECEIVE_API_FILENAME)
    content = "This is a test in pytest!"
    
    # Generate temporary file
    with open(source_path, "w") as file:
        file.write(content)
    
    # Send file to endpoint
    with open(source_path, "rb") as file:
        response = client.post(RECEIVE_URL,
                               data={'file': file})
        assert response.status_code == 201
    
    # Check if received file is the same
    with open(dest_path, "r") as file:
        assert file.read() == content
    
    # Delete generated files
    os.remove(source_path)
    os.remove(dest_path)


def test_receive_file__wrong_post(client):
    response = client.post(RECEIVE_URL)
    assert response.status_code == 400
