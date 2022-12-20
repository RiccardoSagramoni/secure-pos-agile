from communication import RestServer
from communication.api.file import ReceiveFileApi
from communication.api.json import ReceiveJsonApi


if __name__ == "__main__":
    server = RestServer()
    server.api.add_resource(ReceiveFileApi,
                            "/",
                            resource_class_kwargs={'filename': 'file.txt'})
    server.api.add_resource(ReceiveJsonApi,
                            "/json",
                            resource_class_kwargs={'filename': 'received_json.json'})
    server.run(debug=True)
