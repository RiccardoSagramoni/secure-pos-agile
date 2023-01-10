import json
import logging
import threading

from communication import RestServer
from communication.api.json_transfer import ReceiveJsonApi
from factory.raw_session_factory import RawSessionFactory
from preparation_system.prepared_session_generator import PreparedSessionGenerator
from preparation_system.prepared_session_sender import PreparedSessionSender
from preparation_system.raw_session_sanitizer import RawSessionSanitizer
from utility.json_validation import validate_json


class PreparationSystemController:

    def __init__(self):
        self.config_path = "../../data/preparation_system/conf/conf.json"
        self.config_schema_path = "../../data/preparation_system/conf/config_schema.json"
        self.config = None

    def send_prepared_session(self, prepared_session_dict):
        if self.config["mode"] == "development":
            # mando la prepared session al segregation system
            url = 'http://' + self.config["ip_segregation_system"] +\
                  ':' + self.config["port_segregation_system"]
            logging.info("Send prepared session to segregation system")
        else:
            # mando la prepared session all'execution system
            url = 'http://' + self.config["ip_execution_system"] +\
                  ':' + self.config["port_execution_system"]
            logging.info("Send prepared session to execution system")
        sender = PreparedSessionSender(url)
        sender.send_prepared_session(prepared_session_dict)

    def generate_prepared_session(self, raw_session):
        logging.info("Start prepared session generation")
        prepared_session_generator = PreparedSessionGenerator(raw_session)
        prepared_session_dict = prepared_session_generator.extract_features()
        self.send_prepared_session(prepared_session_dict)

    def processing_raw_session(self, raw_session_json):
        logging.info("Processing raw session")
        raw_session = RawSessionFactory.generate_from_dict(raw_session_json)
        sanitizer = RawSessionSanitizer(raw_session, self.config["minimum_amount_possible"],
                                        self.config["maximum_amount_possible"])

        sanitizer.correct_missing_time()
        sanitizer.correct_missing_amount()
        logging.info("Corrected missing attributes")

        sanitizer.correct_outliers()
        logging.info("Corrected outliers")

        self.generate_prepared_session(sanitizer.raw_session)

    def handle_message(self, raw_session_json):
        # When the system receives a message, generate a new thread
        logging.info("Received raw session")
        thread = threading.Thread(target=self.processing_raw_session,
                                  args=[raw_session_json])
        thread.start()

    def start_server(self):
        # Instantiate server
        logging.info("Start server for receiving raw sessions")
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
        if not validate_json(config, config_schema):
            logging.error("Impossible to load the preparation system "
                          "configuration: JSON file is not valid")
            raise ValueError("Preparation System configuration failed")
        logging.info("Preparation System configured correctly")
        self.config = config

    def run(self):
        # carico la configurazione
        self.load_config()

        # mi metto in attesa di ricevere le raw session
        self.start_server()
