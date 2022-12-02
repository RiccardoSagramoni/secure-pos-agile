import pytest
from flask import Flask

from communication import create_app
from communication.api import *


@pytest.fixture
def app() -> Flask:
    resources = [
        (EchoApi, "/"),
        (GetFileApi, "/get/<filename>")
    ]
    return create_app(resources)


def test_start(app, client):
    assert client.get('/').status_code == 200


def test2(app, client):
    assert client.get('/get/label.csv').status_code == 200
