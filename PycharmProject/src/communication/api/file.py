import os

import flask
from flask_restful import Resource

from utility import get_project_folder


class GetFileApi(Resource):
    """
    This API allows to expose a file in the server's file system via GET method.
    """
    
    def __init__(self, filename: str):
        """
        Initialize the API by setting the folder path.
        :param filename: relative path from the project folder.
        """
        self.filename = os.path.realpath(get_project_folder() + filename)
    
    def get(self):
        """
        Get the file offered by the endpoint.
        :return: the server response: an error message on failure, the requested file on success.
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
        self.directory = os.path.realpath(get_project_folder() + directory)
    
    def get(self, filename: str):
        """
        Get any file from the base folder.
        :param filename: name of the file
        :return: the server response: an error message on failure, the requested file on success.
        """
        return flask.send_from_directory(directory=self.directory, path=filename, as_attachment=True)
