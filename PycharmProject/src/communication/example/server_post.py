from communication import RestServer
from communication.api.file import ReceiveFileApi


if __name__ == "__main__":
    server = RestServer()
    server.api.add_resource(ReceiveFileApi,
                            "/",
                            resource_class_kwargs={'filename': 'file.txt'})
    server.run(debug=True)
