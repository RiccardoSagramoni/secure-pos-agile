import pytest
from flask import Flask

from communication import create_app
from communication.api import EchoApi, GetFileApi

echo_addr = '/'
get_file_addr = '/file'


@pytest.fixture
def app() -> Flask:
    resources = [
        (EchoApi, echo_addr),
        (GetFileApi, get_file_addr + "/<filename>")
    ]
    return create_app(resources)


def test_get_echo_api(client):
    r = client.get(echo_addr)
    assert r.status_code == 200
    assert 'Hello World' == r.json


def test_post_echo_api(client):
    sent_json = {"name": "value"}
    r = client.post(echo_addr, json=sent_json)
    assert r.status_code == 201
    assert {"you sent": sent_json} == r.json


def test_get_getfile_api(client):
    r = client.get('/file/label.csv')
    assert r.status_code == 200
    assert 'event_id' in r.text
    assert 'label' in r.text
