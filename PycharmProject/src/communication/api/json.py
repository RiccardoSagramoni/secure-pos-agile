import json
import os

from flask import request
from flask_restful import Resource


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
