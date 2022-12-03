from typing import List

from flask import Flask
from flask_restful import Api


def create_app(resource_list: List[tuple]) -> Flask:
    app = Flask(__name__)
    api = Api(app)
    
    for (resource, *url) in resource_list:
        api.add_resource(resource, *url)
    
    return app


def run_app(app: Flask, host: str = "0.0.0.0", port: int = 80, debug: bool = False) -> None:
    app.run(host=host, port=port, debug=debug)
