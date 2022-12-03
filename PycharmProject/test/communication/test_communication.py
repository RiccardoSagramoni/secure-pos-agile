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
    return server.app


def test_get_echo_api(client):
    r = client.get(echo_url)
    assert r.status_code == 200
    assert 'Hello World' == r.json


def test_post_echo_api(client):
    sent_json = {"name": "value"}
    r = client.post(echo_url, json=sent_json)
    assert r.status_code == 201
    assert {"you sent": sent_json} == r.json


def test_get_getfile_api(client):
    r = client.get(getfile_url + '/label.csv')
    assert r.status_code == 200
    assert 'event_id' in r.text
    assert 'label' in r.text
