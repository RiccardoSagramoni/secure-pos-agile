import pytest
from flask import Flask

from communication import RestServer
from communication.api import EchoApi
from communication.api.csv_transfer import GetCSVApi, GetCSVInsideDirectoryApi
from communication.api.file import ReceiveFileApi, GetFileApi, GetFilesInsideDirectoryApi
from communication.api.json_transfer import GetJsonApi, GetJsonInsideDirectoryApi, ReceiveJsonApi

# echo api url
ECHO_URL = '/'
# file api urls
RECEIVE_URL = '/send_file'
GETFILE_URL = '/file'
GETFILE_DIR_URL = '/dir'
# json file urls
RECEIVE_JSON_URL = '/send_json'
GET_JSON_URL = '/json'
GET_JSON_DIR_URL = '/json_dir'
# ccsv file urls
GET_CSV_URL = '/csv'
GET_CSV_DIR_URL = '/csv_dir'

RECEIVE_API_FILENAME = 'test/communication/receive.txt'
RECEIVE_API_JSON_FILENAME = 'test/communication/received.json'


@pytest.fixture(scope='package')
def app() -> Flask:
    server = RestServer()
    server.api.add_resource(EchoApi, ECHO_URL)

    server.api.add_resource(ReceiveFileApi,
                            RECEIVE_URL,
                            resource_class_kwargs={'filename': RECEIVE_API_FILENAME})
    server.api.add_resource(GetFileApi,
                            GETFILE_URL,
                            resource_class_kwargs={'filename': 'data/label.csv'})
    server.api.add_resource(GetFilesInsideDirectoryApi,
                            GETFILE_DIR_URL + "/<filename>",
                            resource_class_kwargs={'directory': 'data/'})

    server.api.add_resource(ReceiveJsonApi,
                            RECEIVE_JSON_URL,
                            resource_class_kwargs={'filename': "./../" + RECEIVE_API_JSON_FILENAME, 'json_schema':'demo_received_json_schema.json'})
    server.api.add_resource(GetJsonApi,
                            GET_JSON_URL,
                            resource_class_kwargs={'filename': 'data/example.json'})
    server.api.add_resource(GetJsonInsideDirectoryApi,
                            GET_JSON_DIR_URL + "/<filename>",
                            resource_class_kwargs={'directory': 'data/'})

    server.api.add_resource(GetCSVApi,
                            GET_CSV_URL,
                            resource_class_kwargs={'filename': 'data/network.csv'})
    server.api.add_resource(GetCSVInsideDirectoryApi,
                            GET_CSV_DIR_URL + "/<filename>",
                            resource_class_kwargs={'directory': 'data/'})
    return server.app
