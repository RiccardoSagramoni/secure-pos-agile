from communication import RestServer
from communication.api import EchoApi, GetFileApi

if __name__ == "__main__":
    server = RestServer()
    server.api.add_resource(EchoApi, "/")
    server.api.add_resource(GetFileApi,
                            "/get/<filename>",
                            resource_class_kwargs={'base_path': '../../data/'})
    server.run(debug=True)
