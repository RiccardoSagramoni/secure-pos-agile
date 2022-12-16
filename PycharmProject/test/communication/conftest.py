import pytest
from flask import Flask

from communication import RestServer
from communication.api import EchoApi
from communication.api.csv import ReadCSVApi
from communication.api.file import ReceiveFileApi, GetFileApi, GetFilesInsideDirectoryApi
from communication.api.json import ManageJsonApi

ECHO_URL = '/'
RECEIVE_URL = '/send_file'
GETFILE_URL = '/file'
GETFILE_DIR_URL = '/dir'
JSON_URL = '/json'
CSV_URL = '/csv'

RECEIVE_API_FILENAME = 'test/communication/receive.txt'


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
    server.api.add_resource(ManageJsonApi,
                            JSON_URL + "/<filename>",
                            resource_class_kwargs={'base_path': 'data/'})
    server.api.add_resource(ReadCSVApi,
                            CSV_URL + "<filename>",
                            resource_class_kwargs={'base_path': 'data/'})
    return server.app
