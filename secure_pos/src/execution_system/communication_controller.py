import logging
import threading
import typing
import requests
from datetime import datetime

from communication import RestServer
from communication.api.json_transfer import ReceiveJsonApi
from communication.api.file_transfer import ReceiveFileApi
from execution_system.execution_system_configuration import ExecutionSystemConfiguration

CLASSIFIER_MODEL_PATH = 'execution_system/classifier_model.sav'
SESSION_SCHEMA_PATH = 'execution_system/prepared_session_schema.json'
TESTING_URL = 'http://25.34.31.202:1234'


def send_testing_timestamp(scenario_id: int, session_id: str = None) -> None:
    print("sending testing timestamp")
    # get timestamp and convert to string
    end_timestamp = datetime.strptime(datetime.now(), "%Y-%m-%d %H:%M:%S.%f")
    testing_msg = {
        'scenario_id': scenario_id,
        'session_id': session_id,
        'timestamp': end_timestamp
    }
    response = requests.post(TESTING_URL, json=testing_msg)
    if not response.ok:
        logging.error("Failed to send message to testing:\n%s", testing_msg)


class CommunicationController:

    def __init__(self, conf: ExecutionSystemConfiguration,
                 execution_handler: typing.Callable[[dict], None],
                 deployment_handler: typing.Callable[[dict], None]):
        self.__ip_address = conf.system_ip
        self.__port = conf.system_port
        self.__monitoring_system_url = conf.monitoring_system_url
        self.__execution_handler = execution_handler
        self.__deployment_handler = deployment_handler

    def start_execution_rest_server(self) -> None:
        server = RestServer()

        server.api.add_resource(ReceiveFileApi,
                                "/classifier_model",
                                resource_class_kwargs={
                                    'filename': CLASSIFIER_MODEL_PATH,
                                    'handler': self.handle_message_deployment
                                })

        server.api.add_resource(ReceiveJsonApi,
                                "/",
                                resource_class_kwargs={
                                    'handler': self.handle_message_execution
                                })
        server.run(host=self.__ip_address, port=self.__port, debug=False)

    def handle_message_deployment(self) -> None:
        # Deployment flow
        threading.Thread(
            target=self.__deployment_handler
        ).start()

    def handle_message_execution(self, json_session: dict) -> None:
        # Execution flow
        threading.Thread(
            target=self.__execution_handler,
            args=[json_session]
        ).start()

    def send_attack_risk_label(self, monitoring_label_dict: dict) -> None:
        print("sending label to monitoring")
        response = requests.post(self.__monitoring_system_url, json=monitoring_label_dict)
        if not response.ok:
            logging.error("Failed to send label:\n%s", monitoring_label_dict)
