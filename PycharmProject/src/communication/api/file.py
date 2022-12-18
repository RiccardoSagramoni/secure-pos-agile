import os
from typing import Callable

import flask
from flask import request
from flask_restful import Resource

from utility import get_project_folder


class ReceiveFileApi(Resource):
    def __init__(self,
                 filename: str,
                 handler: Callable[[], None] = None):
        self.filename = os.path.join(get_project_folder(), filename)
        self.handle_request = handler
    
    def post(self):
        if 'file' not in request.files:
            return flask.abort(400)
            
        file = request.files['file']
        file.save(self.filename)
        
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
        return flask.send_from_directory(directory=self.directory, path=filename, as_attachment=True)
