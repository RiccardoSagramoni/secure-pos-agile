import logging
import os
import json

import requests
import utility

from communication import RestServer
from communication.api.json_transfer import ReceiveJsonApi

ML_SETS_JSON_FILE_PATH = 'development_system/received_files/ml_set_for_training_classifier.json'

class CommunicationController:

    def __init__(self, developing_system_configuration, development_system_controller):

        self.ip_address = developing_system_configuration.ip_address
        self.port = developing_system_configuration.port
        self.segregation_system_url = developing_system_configuration.segregation_system_url
        self.execution_system_url = developing_system_configuration.execution_system_url
        self.development_system_controller = development_system_controller

    def handle_message(self, json_record: dict) -> None:

        with open(os.path.join(utility.data_folder, ML_SETS_JSON_FILE_PATH), 'w') as file_to_save:
            json.dump(json_record, file_to_save, indent=2)

        self.development_system_controller.identify_the_top_mlp_classifiers()

    def start_developing_rest_server(self) -> None:

        server = RestServer()
        server.api.add_resource(ReceiveJsonApi,
                                "/",
                                resource_class_kwargs={
                                    'handler': self.handle_message
                                })
        server.run(host=self.ip_address, port=self.port, debug=False)


    def send_classifier_to_execution_system(self, classifier_path):
        with open(classifier_path, 'rb') as file_to_send:
            response = requests.post(self.execution_system_url, files={'file': file_to_send})
        if not response.ok:
            logging.error("Failed to send the classifier to the execution system")