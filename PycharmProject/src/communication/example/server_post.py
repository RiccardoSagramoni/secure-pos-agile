from communication import RestServer
from communication.api.file_transfer import ReceiveFileApi
from communication.api.json_transfer import ReceiveJsonApi


if __name__ == "__main__":
    server = RestServer()
    server.api.add_resource(ReceiveFileApi,
                            "/send_file",
                            resource_class_kwargs={'filename': 'file.txt'})
    server.api.add_resource(ReceiveJsonApi,
                            "/send_json",
                            resource_class_kwargs={
                                'filename': 'demo_received_json.json',
                                'json_schema': 'demo_received_json_schema.json'
                            })
    server.run(debug=True)
