import threading

from communication import RestServer
from communication.api.json_transfer import ReceiveJsonApi
from monitoring_system.LabelManager import LabelManager


class MonitoringSystemController:
    label_manager = LabelManager()

    def __int__(self):
        self.label_manager = LabelManager()

    def handle_message(self):
        # When the system receives a message, generate a new thread
        thread = threading.Thread(target=self.label_manager.store_label)
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
                                    'handler': lambda: self.handle_message()
                                })
        server.run(debug=True)

    def create_tables(self):
        query = "CREATE TABLE expertLabel (sessionId TEXT PRIMARY KEY UNIQUE, value TEXT)"
        self.label_manager.storer.create_table(query)
        query = "CREATE TABLE classifierLabel (sessionId TEXT PRIMARY KEY UNIQUE, value TEXT)"
        self.label_manager.storer.create_table(query)

    def run(self):
        # creo le tabelle per memorizzare le label
        self.create_tables()

        # mi metto in attesa di ricevere le label
        self.start_server()

