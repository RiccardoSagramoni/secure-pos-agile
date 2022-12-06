import os.path
import json

from flask import request, send_file
from flask_restful import Resource
from pandas import read_csv


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
    This API allows to get files from a specified folder,
    by sending a GET request on to endpoint "/<filename>"
    """

    def __init__(self, base_path: str):
        """
        Initialize the API by setting the folder path
        :param base_path: relative or absolute folder path.
        """
        self.base_path = os.path.realpath(base_path)

    def get(self, filename: str):
        """
        Get files from server
        :param filename: name of the file
        :return: the server response: an error message on failure, the requested file on success.
        """
        # Check path traversal
        real_path = os.path.realpath(self.base_path + "/" + filename)
        if not real_path.startswith(self.base_path):
            return "Path traversal detected", 403

        return send_file(real_path, as_attachment=True)


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
