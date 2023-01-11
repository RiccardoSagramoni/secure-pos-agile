"""
This module contains API classes which handle file reception and sending.
In order to use the API, add them as resources to your Flask application.
"""
import os
from typing import Callable

import flask
from flask import request
from flask_restful import Resource

from utility import project_folder


class ReceiveFileApi(Resource):
    """
    This API allows other nodes to send files to the Flask application.
    """
    
    def __init__(self,
                 filename: str,
                 handler: Callable[[], None] = None):
        """
        Initialize the API.
        :param filename: path where to save the received file (relative to the project folder).
        :param handler: optional function to call after the file has been saved in the filesystem.
                        The handler function should not take too much time to return
                        (start a new thread, if necessary).
        """
        self.filename = os.path.join(project_folder, filename)
        self.handle_request = handler
    
    def post(self):
        """
        Handle a POST request.
        Other nodes should send a POST request when they want to send a file to this endpoint.
        The file must be inserted in the ``files['file']`` field of the request.
        :return: status code 201 on success, 400 if the file does not exist
        """
        # Check if the request contains the file
        if 'file' not in request.files:
            return flask.abort(400)
        
        # Save the file in the filesystem
        file = request.files['file']
        file.save(self.filename)
        
        # Execute the handler function if it was specified
        if self.handle_request is not None:
            self.handle_request()
        
        return 'File correctly received', 201
