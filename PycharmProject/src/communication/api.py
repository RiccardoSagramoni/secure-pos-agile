import os.path
import json

from flask import request, send_file, jsonify
from flask_restful import Resource
from pandas import read_csv


class EchoApi(Resource):
    @staticmethod
    def get():
        return "Hello World", 200
    
    @staticmethod
    def post():
        some_json = request.get_json()
        return {"you sent": some_json}, 201


class GetFileApi(Resource):
    
    def __init__(self, base_path: str):
        self.base_path = os.path.realpath(base_path)
    
    def get(self, filename: str):
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

        with open(real_path, "r") as file:
            data = json.load(file)

        return {data}, 200

    def post(self, filename: str):
        real_path = os.path.realpath(self.base_path + "/" + filename)
        if not real_path.startswith(self.base_path):
            return "Path traversal detected", 403

        some_json = request.get_json()
        ip_address = request.remote_addr
        print(f" JSON Received: {some_json} From: {ip_address}")
        with open(real_path, "a") as file:
            json.dump(some_json, file)

        return {'OK'}, 201

class ReadCSVApi(Resource):
    def __init__(self, base_path: str):
        self.base_path = os.path.realpath(base_path)

    def get(self, filename: str):
        real_path = os.path.realpath(self.base_path + "/" + filename)
        if not real_path.startswith(self.base_path):
            return "Path traversal detected", 403

        with open(real_path, "r") as file:
            data = read_csv(file)
            data = data.to_dict()

        return {data}, 200
