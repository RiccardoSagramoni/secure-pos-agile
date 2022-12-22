"""
This module contains API classes which handle file reception and sending.
In order to use the API, add them as resources to your Flask application.
"""
import os
from typing import Callable

import flask
from flask import request
from flask_restful import Resource

from utility import get_project_folder, get_received_data_folder


class ReceiveFileApi(Resource):
    """
    This API allows other nodes to send files to the Flask application.
    """
    
    def __init__(self,
                 filename: str,
                 handler: Callable[[], None] = None):
        """
        Initialize the API.
        :param filename: path where to save the received file (relative to the received data folder).
        :param handler: optional function to call after the file has been saved in the filesystem.
                        The handler function should not take too much time to return
                        (start a new thread, if necessary).
        """
        self.filename = os.path.join(get_received_data_folder(), filename)
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


class GetFileApi(Resource):
    """
    This API allows to expose a file in the server's file system via GET method.
    """
    
    def __init__(self, filename: str):
        """
        Initialize the API by setting the folder path.
        :param filename: relative path from the project folder.
        """
        self.filename = os.path.join(get_project_folder(), filename)
    
    def get(self):
        """
        Get the file exposed by the endpoint.
        :return: the server response: on success return status 200 and the exposed file,
                 on failure return status 404 and an error message
        """
        try:
            return flask.send_file(self.filename, as_attachment=True)
        except FileNotFoundError:
            return flask.abort(404)


class GetFilesInsideDirectoryApi(Resource):
    """
    This API allows to get files from a specified folder,
    by sending a GET request on to endpoint "/<filename>"
    """
    
    def __init__(self, directory: str):
        """
        Initialize the API by setting the folder path.
        :param directory: relative path from the project folder.
        """
        self.directory = os.path.join(get_project_folder(), directory)
    
    def get(self, filename: str):
        """
        Get any file from the directory.
        :param filename: name of the file
        :return: the server response: on success return status 200 and the exposed file,
                 on failure return status 404 and an error message
        """
        return flask.send_from_directory(directory=self.directory,
                                         path=filename,
                                         as_attachment=True)
