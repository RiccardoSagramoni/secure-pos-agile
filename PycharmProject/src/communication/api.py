from flask import request, send_file
from flask_restful import Resource
import os.path


class EchoApi(Resource):
    def get(self):
        return "Hello World", 200
    
    def post(self):
        some_json = request.get_json()
        return {"you sent": some_json}, 201


class GetFileApi(Resource):
    base_path = os.path.realpath("../../data/")
    
    def get(self, filename):
        # Check path traversal
        real_path = os.path.realpath(self.base_path + "/" + filename)
        if not real_path.startswith(self.base_path):
            return "Path traversal detected", 403
        
        return send_file(real_path, as_attachment=True)


'''
X echo
X file (classifier)
- json
- csv
'''