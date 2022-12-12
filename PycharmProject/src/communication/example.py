from communication import RestServer
from communication.api import EchoApi, GetFileApi, GetFilesInsideDirectoryApi, ManageJsonApi, ReadCSVApi

if __name__ == "__main__":
    # Instantiate server
    server = RestServer()
    
    # Add APIs
    server.api.add_resource(EchoApi, "/")
    server.api.add_resource(GetFileApi, "/file",
                            resource_class_kwargs={'filename': '/data/labbbel.csv'})
    server.api.add_resource(GetFilesInsideDirectoryApi,
                            "/dir/<filename>",
                            resource_class_kwargs={'directory': '/data/'})
    server.api.add_resource(ManageJsonApi,
                            "/json/<filename>",
                            resource_class_kwargs={'base_path': '/data/'})
    server.api.add_resource(ReadCSVApi,
                            "/csv/<filename>",
                            resource_class_kwargs={'base_path': '/data/'})
    # Start server
    server.run(debug=True)
