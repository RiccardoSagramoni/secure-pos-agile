import json
import threading

from communication import RestServer
from communication.api.json_transfer import ReceiveJsonApi
from monitoring_system.label_manager import LabelManager
from utility.json_validation import validate_json


class MonitoringSystemController:

    def __init__(self):
        self.label_manager = LabelManager()
        self.config_path = "./conf/config.json"
        self.config_schema_path = "./conf/config_schema.json"
        self.config = None

    def handle_message(self, label_json):
        # When the system receives a message, generate a new thread
        thread = threading.Thread(target=self.label_manager.store_label,
                                  args=(self.config["monitoring_window_length"], label_json))
        thread.start()

    def start_server(self):
        # Path where to save the received file containing the label in json format
        filename = 'label.json'

        # Instantiate server
        server = RestServer()
        server.api.add_resource(ReceiveJsonApi,
                                "/",
                                resource_class_kwargs={
                                    'filename': filename,
                                    # l'handler gestisce l'archiviazione delle label
                                    'handler': lambda x: self.handle_message(x)
                                })
        server.run(debug=True)

    def create_tables(self):
        query = "CREATE TABLE if not exists expertLabel" \
                "(session_id TEXT PRIMARY KEY UNIQUE, value TEXT)"
        self.label_manager.storer.create_table(query)
        query = "CREATE TABLE if not exists classifierLabel" \
                "(session_id TEXT PRIMARY KEY UNIQUE, value TEXT)"
        self.label_manager.storer.create_table(query)

    def load_config(self):
        with open(self.config_path, "r", encoding="UTF-8") as file:
            config = json.load(file)
        with open(self.config_schema_path, "r", encoding="UTF-8") as file:
            config_schema = json.load(file)
        validate_json(config, config_schema)
        self.config = config

    def run(self):
        # carico la configurazione
        self.load_config()

        # creo le tabelle per memorizzare le label
        self.create_tables()

        # mi metto in attesa di ricevere le label
        self.start_server()


if __name__ == "__main__":
    test = MonitoringSystemController()
    test.load_config()
    test.create_tables()
    label = {
            "session_id": 8,
            "source": "expert",
            "value": "attack"
            }
    test.handle_message(label)
