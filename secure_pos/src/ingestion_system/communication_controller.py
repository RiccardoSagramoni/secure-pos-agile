import logging
import threading
import typing

import requests

from communication import RestServer
from communication.api.json_transfer import ReceiveJsonApi
from data_objects.attack_risk_label import AttackRiskLabel
from data_objects.raw_session import RawSession
from ingestion_system.configuration import Configuration
from ingestion_system.data_object_packagers import RawSessionPackager, AttackRiskLabelPackager

RECORD_SCHEMA_PATH = "ingestion_system/records_schema.json"


class CommunicationController:
    """
    Class responsible for:
    
    - Configuring and start a REST endpoint
    - Receiving transaction records in JSON format from the client-side systems
      and starting a thread for the ingestion process
    - Sending the raw sessions to the preparation system and the attack risk labels
      to the monitoring system.
    """
    
    def __init__(self, conf: Configuration, handler: typing.Callable[[dict], None]):
        self.__ip_address = conf.ip_address
        self.__port = conf.port
        self.__preparation_system_url = conf.preparation_system_url
        self.__monitoring_system_url = conf.monitoring_system_url
        self.__request_handler = handler
    
    def start_ingestion_rest_server(self) -> None:
        """
        Configure and start REST endpoint.
        """
        # Configure the REST server
        server = RestServer()
        server.api.add_resource(ReceiveJsonApi,
                                "/",
                                resource_class_kwargs={
                                    'json_schema_path': RECORD_SCHEMA_PATH,
                                    'handler': self.handle_message
                                })
        # Start the REST server
        server.run(host=self.__ip_address, port=self.__port)
    
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
        """
        Send a raw session in JSON format to the preparation system.
        :param raw_session: RawSession object to package and send
        """
        # Serialize raw session
        raw_session_dict = RawSessionPackager(raw_session).package_as_json_dict()
        # Send serialized raw session
        try:
            response = requests.post(self.__preparation_system_url, json=raw_session_dict)
            if not response.ok:
                logging.error("Failed to send raw session %s", raw_session.session_id)
        except requests.exceptions.RequestException as ex:
            logging.error("Unable to send raw session %s.\tException %s", raw_session.session_id, ex)
    
    def send_attack_risk_label(self, session_id: str, attack_risk_label: AttackRiskLabel) -> None:
        """
        Send an attack risk label to the monitoring system.
        :param session_id: id of the session
        :param attack_risk_label: label
        """
        # Serialize attack risk label
        label_dict = AttackRiskLabelPackager(session_id, attack_risk_label)
        # Send serialized label
        logging.info("Send session %s", session_id)
        try:
            response = requests.post(self.__monitoring_system_url, json=label_dict)
            if not response.ok:
                logging.error("Failed to send label:\n%s", label_dict)
        except requests.exceptions.RequestException as ex:
            logging.error("Unable to send raw session %s.\tException %s", session_id, ex)
