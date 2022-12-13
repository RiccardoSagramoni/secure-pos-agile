import pytest
from flask import Flask

from communication import RestServer
from communication.api import EchoApi
from communication.api.file import GetFilesInsideDirectoryApi

ECHO_URL = '/'
GETFILE_URL = '/get'


@pytest.fixture(scope='session')
def app() -> Flask:
    server = RestServer()
    server.api.add_resource(EchoApi, ECHO_URL)
    server.api.add_resource(GetFilesInsideDirectoryApi,
                            GETFILE_URL + "/<filename>",
                            resource_class_kwargs={'directory': '/data/'})
    return server.app


def test_echo_api__get(client):
    response = client.get(ECHO_URL)
    assert response.status_code == 200
    assert 'Hello World' == response.json


def test_echo_api__post(client):
    sent_json = {"name": "value"}
    response = client.post(ECHO_URL, json=sent_json)
    assert response.status_code == 201
    assert response.json == {"you sent": sent_json}


def test_getfile_api__get(client):
    response = client.get(GETFILE_URL + '/label.csv')
    assert response.status_code == 200


def test_getfile_api__wrong_file(client):
    response = client.get(GETFILE_URL + '/wrong.file')
    assert response.status_code == 404
