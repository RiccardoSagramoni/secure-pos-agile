"""
This module offers a set of classes to easily deploy a REST server.
"""

from flask import Flask
from flask_restful import Api


class RestServer:
    """
    This class stores the central object of a Flask Application
    and provides direct access to its API.
    """
    
    def __init__(self, name: str = __name__):
        """
        Initialize a Flask Application.
        :param name: name of the application.
        """
        self._app = Flask(name)
        self.api = Api(self._app)
    
    def run(self, host: str = "0.0.0.0", port: int = 8000, debug: bool = False) -> None:
        """
        Runs the Flask Application on a local development server.
        
        :param host: the hostname to listen to. Defaults to 0.0.0.0.
        :param port: the port of the web server. Defaults to 8000.
        :param debug: enable or disable debug mode. Disabled by default.
        """
        self._app.run(host=host, port=port, debug=debug)
