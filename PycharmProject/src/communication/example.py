from communication import RestServer
from communication.api import EchoApi, GetFileApi, ManageJsonApi, ReadCSVApi

if __name__ == "__main__":
    # Instantiate server
    server = RestServer()
    # Add APIs
    server.api.add_resource(EchoApi, "/")
    server.api.add_resource(GetFileApi,
                            "/get/<filename>",
                            resource_class_kwargs={'base_path': '../../data/'})
    server.api.add_resource(ManageJsonApi,
                            "/json/<filename>",
                            resource_class_kwargs={'base_path': '../../data/'})
    server.api.add_resource(ReadCSVApi,
                            "/csv/<filename>",
                            resource_class_kwargs={'base_path': '../../data/'})
    # Start server
    server.run(debug=True)
