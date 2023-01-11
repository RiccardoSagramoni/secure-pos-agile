import json
import logging
import threading

from communication import RestServer
from communication.api.json_transfer import ReceiveJsonApi
from monitoring_system.label_manager import LabelManager
from utility.json_validation import validate_json


class MonitoringSystemController:

    def __init__(self):
        self.label_manager = LabelManager()
        self.config_path = "../../data/monitoring_system/conf/config.json"
        self.config_schema_path = "../../data/monitoring_system/conf/config_schema.json"
        self.config = None

    def handle_message(self, label_json):
        # When the system receives a message, generate a new thread
        logging.info("Received label")
        thread = threading.Thread(target=self.label_manager.store_label,
                                  args=(self.config["monitoring_window_length"], label_json))
        thread.start()

    def start_server(self):
        # Instantiate server
        logging.info("Start server for receiving labels")
        server = RestServer()
        server.api.add_resource(ReceiveJsonApi,
                                "/",
                                resource_class_kwargs={
                                    # l'handler gestisce l'archiviazione delle label
                                    'handler': self.handle_message
                                })
        server.run(debug=True, port=8001)

    def create_tables(self):
        logging.info("Create tables (if not exists) for label storage")
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
        if not validate_json(config, config_schema):
            logging.error("Impossible to load the monitoring system "
                          "configuration: JSON file is not valid")
            raise ValueError("Monitoring System configuration failed")
        logging.info("Monitoring System configured correctly")
        self.config = config

    def run(self):
        # carico la configurazione
        self.load_config()

        # creo le tabelle per memorizzare le label
        self.create_tables()

        # mi metto in attesa di ricevere le label
        self.start_server()
