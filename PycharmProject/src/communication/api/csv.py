import os

from flask_restful import Resource
from pandas import read_csv


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
