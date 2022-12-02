from pandas import read_csv
from flask import request, send_file
from flask_restful import Resource
import json


class EchoApi(Resource):
    file_path = '../data/label.csv'
    
    def get(self):
        data = read_csv(self.file_path).to_dict()
        return {'data': data}, 200
    
    def post(self):
        some_json = request.get_json()
        return {"you sent": some_json}, 201


class GetFileApi(Resource):
    file_path = 'classifier.gz'
    
    def get(self):
        return send_file(self.file_path, as_attachment=True)

