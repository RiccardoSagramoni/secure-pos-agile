import logging
import threading
import requests

from communication import RestServer
from communication.api.json_transfer import ReceiveJsonApi


class CommunicationController:
    """
    Class that manage all the communication with other systems
    """

    def __init__(self, db_handler, url, segregation_system_controller):
        self.filename = './database/PreparedSession.json'
        self.db_handler = db_handler
        self.dev_system_url = url
        self.segregation_system_controller = segregation_system_controller

    def init_rest_server(self):
        """
        Method that create the server waiting for prepared sessions
        """
        server = RestServer()
        server.api.add_resource(ReceiveJsonApi,
                                "/",
                                resource_class_kwargs={
                                    'handler': self.handle_message,
                                })
        server.run()

    def handle_message(self, file_json):
        """
        Method that handle the incoming messages (preparation system)
        """
        logging.info("received new session")
        thread = threading.Thread(target=self.segregation_system_controller.manage_message,
                                  args=[file_json])
        thread.start()

    def send_datasets(self, json_to_send):
        """
        Method that sends the generated datasets to the development system
        :param json_to_send: data to send
        """
        try:
            response = requests.post(self.dev_system_url, json=json_to_send)
            if not response.ok:
                logging.error("Failed to send raw dataset")
        except requests.exceptions.RequestException as ex:
            logging.error("Unable to send raw datasets.\tException %s", ex)
