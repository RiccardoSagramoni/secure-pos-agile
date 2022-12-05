from communication import RestServer
from communication.api import EchoApi, GetFileApi, ManageJsonApi, ReadCSVApi

if __name__ == "__main__":
    server = RestServer()
    server.api.add_resource(EchoApi, "/")
    server.api.add_resource(GetFileApi,
                            "/get/<filename>",
                            resource_class_kwargs={'base_path': '../../data/'})
    server.api.add_resource(ManageJsonApi, "/json/<filename>",
                            resource_class_kwargs={'base_path': '../../data/json/'})
    server.api.add_resource(ReadCSVApi, "/csv/<filename>",
                            resource_class_kwargs={'base_path': '../../data/'})
    server.run(debug=True)
