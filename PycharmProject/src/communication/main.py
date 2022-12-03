from communication import create_app, run_app
from communication.api import EchoApi, GetFileApi

if __name__ == "__main__":
    resources = [
        (EchoApi, "/"),
        (GetFileApi, "/file/<filename>")
    ]
    run_app(create_app(resources), debug=True)
