from communication import RestServer
from communication.api import EchoApi, GetFileApi, ManageJsonApi, ReadCSVApi


def main():
    # Instantiate server
    server = RestServer()

    # Send hello message to slave_json
    print("Expose hello resource")
    server.api.add_resource(EchoApi, "/Hello")

    print("Expose json resource")
    server.api.add_resource(ManageJsonApi,
                            "/json/example.json",
                            resource_class_kwargs={'base_path': '../../data',
                                                   'filename': 'example.json'})

    print("Expose csv resource")
    server.api.add_resource(ReadCSVApi,
                            "/csv/commercial.csv",
                            resource_class_kwargs={'base_path': '../../data/',
                                                   'filename': 'commercial.csv'})

    print("Expose generic resource")
    server.api.add_resource(GetFileApi,
                            "/file/example.json",
                            resource_class_kwargs={'base_path': '../../data/',
                                                   'filename': 'example.json'})
    server.run(debug=True)


if __name__ == "__main__":
    main()
