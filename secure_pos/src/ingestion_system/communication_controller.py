import logging
import threading
import typing

import requests

from communication import RestServer
from communication.api.json_transfer import ReceiveJsonApi
from data_objects.attack_risk_label import AttackRiskLabel
from data_objects.raw_session import RawSession
from ingestion_system.configuration import Configuration
from ingestion_system.data_objects_converters import RawSessionConverter, AttackRiskLabelConverter

RECORD_SCHEMA_PATH = "ingestion_system/records_schema.json"


class CommunicationController:
    
    def __init__(self, conf: Configuration, handler: typing.Callable[[dict], None]):
        self.__ip_address = conf.ip_address
        self.__port = conf.port
        self.__preparation_system_url = conf.preparation_system_url
        self.__monitoring_system_url = conf.monitoring_system_url
        self.__request_handler = handler
    
    def start_ingestion_rest_server(self) -> None:
        server = RestServer()
        server.api.add_resource(ReceiveJsonApi,
                                "/",
                                resource_class_kwargs={
                                    'json_schema': RECORD_SCHEMA_PATH,
                                    'handler': self.handle_message
                                })
        server.run(host=self.__ip_address, port=self.__port, debug=False)
    
    def handle_message(self, json_record: dict) -> None:
        """
        Start a new thread which stores the received record.
        :param json_record: data received from a client-side system.
        """
        threading.Thread(
            target=self.__request_handler,
            args=[json_record]
        ).start()
    
    def send_raw_session(self, raw_session: RawSession) -> None:
        # Serialize raw session
        raw_session_dict = RawSessionConverter(raw_session).convert_to_json_dict()
        response = requests.post(self.__preparation_system_url, json=raw_session_dict)
        if not response.ok:
            logging.error("Failed to send raw session:\n%s", raw_session_dict)
    
    def send_attack_risk_label(self, session_id: str, attack_risk_label: AttackRiskLabel) -> None:
        label_dict = AttackRiskLabelConverter(session_id, attack_risk_label)
        response = requests.post(self.__monitoring_system_url, json=label_dict)
        if not response.ok:
            logging.error("Failed to send label:\n%s", label_dict)
