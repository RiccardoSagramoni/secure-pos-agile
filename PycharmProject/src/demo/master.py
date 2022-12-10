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
                            "/json/<filename>",
                            resource_class_kwargs={'base_path': '../../data'})

    print("Expose csv resource")
    server.api.add_resource(ReadCSVApi,
                            "/csv/<filename>",
                            resource_class_kwargs={'base_path': '../../data/'})

    print("Expose generic resource")
    server.api.add_resource(GetFileApi,
                            "/file/<filename>",
                            resource_class_kwargs={'base_path': '../../data/'})
    server.run(debug=True)


if __name__ == "__main__":
    main()
