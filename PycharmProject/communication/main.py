from communication.rest_server import MyRestServer
from communication.api import *

if __name__ == "__main__":
    resources = [
        (EchoApi, "/echo"),
        (GetFileApi, "/get/<filename>")
    ]
    server = MyRestServer(resources)
    server.start(host="0.0.0.0", port=80, debug=True)
