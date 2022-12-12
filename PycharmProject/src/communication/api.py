import os.path
import json
from os import path

from flask import request, send_file
from flask_restful import Resource
from pandas import read_csv
from utility import get_project_folder


class EchoApi(Resource):
    """
    This REST API implements an echo server:
    
    - GET: send back a message.
    - POST: send back the received data.
    """
    
    @staticmethod
    def get():
        return "Hello World", 200
    
    @staticmethod
    def post():
        some_json = request.get_json()
        return {"you sent": some_json}, 201


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


class ManageJsonApi(Resource):
    def __init__(self, base_path: str):
        self.base_path = os.path.realpath(base_path)
    
    def get(self, filename: str):
        real_path = os.path.realpath(self.base_path + "/" + filename)
        if not real_path.startswith(self.base_path):
            return "Path traversal detected", 403
        
        with open(real_path, "r", encoding="UTF-8") as file:
            data = json.load(file)
        
        return data, 200
    
    def post(self, filename: str):
        real_path = os.path.realpath(self.base_path + "/" + filename)
        if not real_path.startswith(self.base_path):
            return "Path traversal detected", 403
        
        some_json = request.get_json()
        ip_address = request.remote_addr
        print(f" JSON Received: {some_json} From: {ip_address}")
        
        with open(real_path, "w", encoding="UTF-8") as file:
            json.dump(some_json, file, indent=2)
        
        return 'OK', 201


class ReadCSVApi(Resource):
    def __init__(self, base_path: str):
        self.base_path = os.path.realpath(base_path)
    
    def get(self, filename: str):
        real_path = os.path.realpath(self.base_path + "/" + filename)
        if not real_path.startswith(self.base_path):
            return "Path traversal detected", 403
        
        with open(real_path, "r", encoding="UTF-8") as file:
            data = read_csv(file)
            data = data.to_dict()
        
        return data, 200
