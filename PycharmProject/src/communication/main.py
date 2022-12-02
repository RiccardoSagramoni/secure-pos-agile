from communication import *
from communication.api import *

if __name__ == "__main__":
    resources = [
        (EchoApi, "/"),
        (GetFileApi, "/get/<filename>")
    ]
    run_app(create_app(resources))
