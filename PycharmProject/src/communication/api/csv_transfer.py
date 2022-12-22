import os

from pandas import read_csv

import flask
from flask_restful import Resource

from utility import get_project_folder


class GetCSVApi(Resource):
    """
    This API allows to show the content of a csv file in the server's file system via GET method.
    """
    def __init__(self, filename: str):
        """
        Initialize the API by setting the folder path.
        :param filename: relative path from the project folder.
        """
        self.filename = os.path.join(get_project_folder(), filename)

    def get(self):
        """
        Get the content of the csv file by the endpoint.
        :return: the server response: on success return status 200
                 and the content of the csv file,
                 on failure return status 404 and an error message
        """
        try:

            with open(self.filename, "r", encoding="UTF-8") as csv_file:
                data = read_csv(csv_file)
                data = data.to_dict()
                return data, 200

        except FileNotFoundError:
            return flask.abort(404)


class GetCSVInsideDirectoryApi(Resource):
    """
    This API allows to show the content of a csv file in the server's file system via GET method.
    """
    def __init__(self, directory: str):
        """
        Initialize the API by setting the folder path.
        :param directory: relative path from the project folder.
        """
        self.directory = os.path.join(get_project_folder(), directory)

    def get(self, filename: str):
        """
        Get the content of the csv file by the endpoint.
        :return: the server response: on success return status 200 and the show the content of the csv file,
                 on failure return status 404 and an error message
        """
        try:
            with open(os.path.join(self.directory, filename), 'r', encoding="UTF-8") as csv_file:
                data = read_csv(csv_file)
                data = data.to_dict()
                return data, 200

        except FileNotFoundError:
            return flask.abort(404)