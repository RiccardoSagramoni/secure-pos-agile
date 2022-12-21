from communication import RestServer
from communication.api import EchoApi
from communication.api.file import GetFileApi, GetFilesInsideDirectoryApi
from communication.api.json import GetJsonApi, GetJsonInsideDirectoryApi
from communication.api.csv import GetCSVApi, GetCSVInsideDirectoryApi

if __name__ == "__main__":
    # Instantiate server
    server = RestServer()
    
    # Add APIs
    server.api.add_resource(EchoApi, "/")
    server.api.add_resource(GetFileApi,
                            "/file",
                            resource_class_kwargs={'filename': 'data/label.csv'})
    server.api.add_resource(GetFilesInsideDirectoryApi,
                            "/dir/<filename>",
                            resource_class_kwargs={'directory': 'data/'})
    server.api.add_resource(GetJsonApi,
                            "/json",
                            resource_class_kwargs={'filename': 'data/example.json'})
    server.api.add_resource(GetJsonInsideDirectoryApi,
                            "/json_dir/<filename>",
                            resource_class_kwargs={'directory': 'data/'})
    server.api.add_resource(GetCSVApi,
                            "/csv",
                            resource_class_kwargs={'filename': 'data/network.csv'})
    server.api.add_resource(GetCSVInsideDirectoryApi,
                            "/csv_dir/<filename>",
                            resource_class_kwargs={'directory': 'data/'})
    # Start server
    server.run(debug=True)
