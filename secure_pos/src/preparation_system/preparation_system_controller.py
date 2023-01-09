import json
import threading

import pandas

from communication import RestServer
from communication.api.json_transfer import ReceiveJsonApi
from data_objects.raw_session import RawSession
from preparation_system.prepared_session_generator import PreparedSessionGenerator
from preparation_system.prepared_session_sender import PreparedSessionSender
from preparation_system.raw_session_sanitizer import RawSessionSanitizer
from utility.json_validation import validate_json


class PreparationSystemController:

    def __init__(self):
        self.config_path = "./conf/conf.json"
        self.config_schema_path = "./conf/config_schema.json"
        self.config = None

    def send_prepared_session(self, prepared_session_dict):
        if self.config["mode"] == "development":
            # mando la prepared session al segregation system
            url = 'http://' + self.config["ip_segregation_system"] +\
                  ':' + self.config["port_segregation_system"]
        else:
            # mando la prepared session all'execution system
            url = 'http://' + self.config["ip_execution_system"] +\
                  ':' + self.config["port_execution_system"]
        sender = PreparedSessionSender(url)
        sender.send_prepared_session(prepared_session_dict)

    def generate_prepared_session(self, raw_session):
        prepared_session_generator = PreparedSessionGenerator(raw_session)
        prepared_session_dict = prepared_session_generator.extract_features()
        self.send_prepared_session(prepared_session_dict)

    def processing_raw_session(self, raw_session):
        sanitizer = RawSessionSanitizer(raw_session)
        sanitizer.detect_missing_attributes()
        sanitizer.correct_missing_attributes()
        sanitizer.detect_outliers()
        sanitizer.correct_outliers()

        self.generate_prepared_session(raw_session)

    def handle_message(self, raw_session_json):
        # When the system receives a message, generate a new thread
        session_id = raw_session_json["session_id"]
        label = raw_session_json["attack_risk_label"]
        transactions = raw_session_json["transactions"]
        session_df = pandas.DataFrame(transactions)
        raw_session = RawSession(session_id, session_df, label)
        thread = threading.Thread(target=self.processing_raw_session,
                                  args=(raw_session,))
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
