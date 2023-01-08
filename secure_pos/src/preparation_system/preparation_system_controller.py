import json
import threading

from communication import RestServer
from communication.api.json_transfer import ReceiveJsonApi
from utility.json_validation import validate_json


class PreparationSystemController:

    def __init__(self):
        self.config_path = "./conf/conf.json"
        self.config_schema_path = "./conf/config_schema.json"
        self.config = None

    def handle_message(self, raw_session_json):
        # When the system receives a message, generate a new thread
        thread = threading.Thread()
        thread.start()

    def start_server(self):
        # Instantiate server
        server = RestServer()
        server.api.add_resource(ReceiveJsonApi,
                                "/",
                                resource_class_kwargs={
                                    # l'handler gestisce l'archiviazione delle label
                                    'handler': lambda x: self.handle_message(x)
                                })
        server.run(debug=True)

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

        # mi metto in attesa di ricevere le raw session
        self.start_server()
