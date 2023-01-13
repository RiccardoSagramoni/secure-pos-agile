import logging
import threading
from datetime import datetime

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
        # DB dropping
        self.db_handler.drop_db()

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


def send_to_testing_system(scenario):
    print(f"Sending scenario: {scenario} to testing system")
    timestamp = datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S.%f")
    # Create a dictionary with requested data
    dictionary = {
        'scenario_id': scenario,
        'timestamp': timestamp
    }
    # Send data
    try:
        response = requests.post('http://25.34.31.202:1234', json=dictionary)
        if not response.ok:
            logging.error("Failed to send raw dataset")
    except requests.exceptions.RequestException as ex:
        logging.error(f"Unable to send scenario msg to testing system.\tException %{ex}\n")
