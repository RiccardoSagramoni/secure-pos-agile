import pytest
from flask import Flask

from communication import RestServer
from communication.api import EchoApi, GetFileApi

echo_url = '/'
getfile_url = '/get'


@pytest.fixture
def app() -> Flask:
    server = RestServer()
    server.api.add_resource(EchoApi, echo_url)
    server.api.add_resource(GetFileApi,
                            getfile_url + "/<filename>",
                            resource_class_kwargs={'base_path': '../../data/'})
    return server._app


def test_get_echo_api(client):
    response = client.get(echo_url)
    assert response.status_code == 200
    assert 'Hello World' == response.json


def test_post_echo_api(client):
    sent_json = {"name": "value"}
    response = client.post(echo_url, json=sent_json)
    assert response.status_code == 201
    assert response.json == {"you sent": sent_json}


def test_get_getfile_api(client):
    response = client.get(getfile_url + '/label.csv')
    assert response.status_code == 200
    assert 'event_id' in response.text
    assert 'label' in response.text
