from communication import RestServer
from communication.api import EchoApi, file, csv, json


def main():
    # Instantiate server
    server = RestServer()

    # Send hello message to slave_json
    print("Expose hello resource")
    server.api.add_resource(EchoApi, "/Hello")

    print("Expose json resource")
    server.api.add_resource(json.ManageJsonApi,
                            "/json/<filename>",
                            resource_class_kwargs={'base_path': '../../data'})

    print("Expose csv resource")
    server.api.add_resource(csv.ReadCSVApi,
                            "/csv/<filename>",
                            resource_class_kwargs={'base_path': '../../data/'})

    print("Expose generic resource")
    server.api.add_resource(file.GetFileApi,
                            "/file",
                            resource_class_kwargs={'filename': '/data/label.csv'})

    server.run(debug=True)


if __name__ == "__main__":
    main()
