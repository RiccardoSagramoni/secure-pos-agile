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

from utility import get_project_folder


class ReceiveJsonApi():
    """
    This API allows other nodes to send json to the Flask application.
    """
    def __init__(self,
                 filename: str,
                 handler: Callable[[], None] = None):
        """
        Initialize the API.
        :param filename: path where to save the received json (relative to PyCharm project folder).
        :param handler: optional function to call after the json has been saved in the filesystem.
                        The handler function should return not take too much time
                        (start a new thread, if necessary).
        """
        self.filename = os.path.join(get_project_folder(), filename)
        self.handle_request = handler

    def post(self):
        """
        Handle a POST request.
        Other nodes should send a POST request when they want to send a json to this endpoint.
        The json must be inserted in the ``json['json_file']`` field of the request.
        :return: status code 201 on success, 400 if the file does not exists
        """
        # Check if the request contains the json file
        if 'json' not in request.json:
            return flask.abort(400)

        some_json = request.get_json()
        ip_address = request.remote_addr
        print(f" JSON Received: {some_json} From: {ip_address}")

        # Save the json in the filesystem
        json.dump(some_json, self.filename, indent=2)

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
        :return: the server response: on success return status 200 and the show the content of the json file,
                 on failure return status 404 and an error message
        """
        try:
            with open(self.filename, 'rb') as json_file:
                json_data = json.load(json_file)
                json_file.close()
                return json_data, 200

        except FileNotFoundError:
            return flask.abort(404)
