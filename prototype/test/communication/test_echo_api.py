from conftest import ECHO_URL


def test_echo_api__get(client):
    response = client.get(ECHO_URL)
    assert response.status_code == 200
    assert 'Hello World' == response.json


def test_echo_api__post(client):
    sent_json = {"name": "value"}
    response = client.post(ECHO_URL, json=sent_json)
    assert response.status_code == 201
    assert response.json == {"you sent": sent_json}
