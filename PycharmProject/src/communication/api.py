import os.path

from flask import request, send_file
from flask_restful import Resource


class EchoApi(Resource):
    @staticmethod
    def get():
        return "Hello World", 200
    
    @staticmethod
    def post():
        some_json = request.get_json()
        return {"you sent": some_json}, 201


class GetFileApi(Resource):

    def __init__(self, base_path):
        self.base_path = os.path.realpath(base_path)
    
    def get(self, filename):
        # Check path traversal
        real_path = os.path.realpath(self.base_path + "/" + filename)
        if not real_path.startswith(self.base_path):
            return "Path traversal detected", 403
        
        return send_file(real_path, as_attachment=True)


'''
X echo
X file
- json
- csv
'''