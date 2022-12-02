from flask import Flask
from flask_restful import Api
from typing import List


class MyRestServer:
    app = Flask(__name__)
    api = Api(app)
    
    def __init__(self, resource_list: List[tuple]):
        for (resource, *url) in resource_list:
            self.api.add_resource(resource, *url)
    
    def start(self, host: str, port: int, debug: bool = False):
        self.app.run(host=host, port=port, debug=debug)
