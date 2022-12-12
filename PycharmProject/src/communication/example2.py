from communication import RestServer
from communication.api.file import GetFileApi

if __name__ == "__main__":
    # Instantiate server
    server = RestServer()
    # Add APIs
    server.api.add_resource(GetFileApi, "/g", resource_class_kwargs={'filename': '/data/geo.csv'})
    server.api.add_resource(GetFileApi, "/1", endpoint="ciao", resource_class_kwargs={'filename': '/data/geggo.csv'})
    server.api.add_resource(GetFileApi, "/2", endpoint="ciao2", resource_class_kwargs={'filename': '/data/label.csv'})
    # Start server
    server.run(debug=True)
