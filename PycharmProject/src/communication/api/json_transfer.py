"""
This module contains API classes which handle json reception and sending.
In order to use the API, add them as resources to your Flask application.
"""
import json
import os
from typing import Callable

import flask
from flask import request
from flask_restful import Resource

from utility import get_project_folder, get_received_data_folder
from utility.json_validation import validate_json_data_file


class ReceiveJsonApi(Resource):
    """
    This API allows other nodes to send json to the Flask application.
    """
    
    def __init__(self,
                 filename: str,
                 json_schema: str = None,
                 handler: Callable[[], None] = None):
        """
        Initialize the API.
        :param filename: path where to save the received json (relative to PyCharm project folder).
        :param handler: optional function to call after the json has been saved in the filesystem.
                        The handler function should not take too much time to return
                        (start a new thread, if necessary).
        """
        self.filename = os.path.join(get_received_data_folder(), filename)
        self.json_schema = json_schema
        self.handle_request = handler
    
    def post(self):
        """
        Handle a POST request.
        Other nodes should send a POST request when they want to send a json to this endpoint.
        The json must be inserted in the ``json['json_file']`` field of the request.
        :return: status code 201 on success, 400 if the file does not exist
        """
        received_json = request.get_json()
        
        # Validate received json
        if self.json_schema is not None \
                and not validate_json_data_file(received_json, self.json_schema):
            return 'JSON validation failed', 400
        
        # Save the json in the filesystem
        with open(self.filename, 'w', encoding="UTF-8") as json_file:
            json.dump(received_json, json_file, indent=2)
        
        # Execute the handler function if it was specified
        if self.handle_request is not None:
            self.handle_request()
        
        return 'JSON correctly received', 201


class GetJsonApi(Resource):
    """
    This API allows to show the content of a json file in the server's file system via GET method.
    """
    
    def __init__(self, filename: str):
        """
        Initialize the API by setting the folder path.
        :param filename: relative path from the project folder.
        """
        self.filename = os.path.join(get_project_folder(), filename)
    
    def get(self):
        """
        Get the content of the json file by the endpoint.
        :return: the server response: on success return status 200
                 and content of the json file,
                 on failure return status 404 and an error message
        """
        try:
            with open(self.filename, 'r', encoding="UTF-8") as json_file:
                json_data = json.load(json_file)
                return json_data, 200
        
        except FileNotFoundError:
            return flask.abort(404)


class GetJsonInsideDirectoryApi(Resource):
    """
    This API allows to show the content of a json file in the server's file system via GET method.
    """
    
    def __init__(self, directory: str):
        """
        Initialize the API by setting the folder path.
        :param directory: relative path from the project folder.
        """
        self.directory = os.path.join(get_project_folder(), directory)
    
    def get(self, filename: str):
        """
        Get the content of the json file by the endpoint.
        :return: the server response: on success return status 200
                 and the content of the json file,
                 on failure return status 404 and an error message
        """
        try:
            with open(os.path.join(self.directory, filename), 'r', encoding="UTF-8") as json_file:
                json_data = json.load(json_file)
                return json_data, 200
        
        except FileNotFoundError:
            return flask.abort(404)
