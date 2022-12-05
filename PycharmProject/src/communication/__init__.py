from flask import Flask
from flask_restful import Api


class RestServer:
    
    def __init__(self, name: str = __name__):
        self.app = Flask(name)
        self.api = Api(self.app)
    
    def run(self, host: str = "0.0.0.0", port: int = 8080, debug: bool = False) -> None:
        self.app.run(host=host, port=port, debug=debug)
