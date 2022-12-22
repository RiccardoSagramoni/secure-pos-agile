from flask import request
from flask_restful import Resource


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
