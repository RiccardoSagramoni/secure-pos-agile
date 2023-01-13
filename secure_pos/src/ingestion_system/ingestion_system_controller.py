import logging

from ingestion_system.communication_controller import CommunicationController
from ingestion_system.configuration import Configuration
from ingestion_system.database_controller import DatabaseController
from ingestion_system.raw_session_sanitizer import RawSessionSanitizer
from ingestion_system.record_synchronizer import RecordSynchronizer
from ingestion_system.system_mode_tracker import SystemModeTracker

CONFIGURATION_FILE_PATH = 'ingestion_system/config.json'
CONFIGURATION_SCHEMA_PATH = 'ingestion_system/config_schema.json'


class IngestionSystemController:
    """
    Class responsible for executing the main logic workflow of the ingestion system.
    
    - It configures the system and all the necessary resources.
    - It handles the reception of a new record.
    """
    
    def __init__(self):
        self.__configuration = Configuration(CONFIGURATION_FILE_PATH, CONFIGURATION_SCHEMA_PATH)
        self.__communication_controller = \
            CommunicationController(self.__configuration, self.handle_new_record_reception)
        self.__system_mode_tracker = \
            SystemModeTracker(self.__configuration)
        self.__database_controller = \
            DatabaseController(self.__configuration, self.__system_mode_tracker)
        self.__record_synchronizer = \
            RecordSynchronizer(self.__database_controller)
    
    def run(self) -> None:
        """
        Start the ingestion system.
        """
        # Start REST server
        self.__communication_controller.start_ingestion_rest_server()
    
    def handle_new_record_reception(self, json_records: dict) -> None:
        """
        Handle a new record whenever it's received by the REST endpoint.
        :param json_records: received JSON data
        """
        # Extract information for logging
        session_id = json_records['session_id']
        record_type = json_records['type']
        logging.info("Received record %s of session %s", record_type, session_id)
        
        # Insert records in database
        ret = self.__database_controller.insert_transaction_record(json_records)
        if not ret:
            logging.error("Impossible to insert records in db: %s", json_records)
            return
        
        # Register received record
        self.__system_mode_tracker.register_record_arrival(session_id)
        
        # Synchronize received record with stored session
        raw_session = self.__record_synchronizer.try_session_synchronization(session_id)
        if raw_session is None:
            logging.info("Session %s is not completed", session_id)
            return
        
        # Sanitize raw session
        RawSessionSanitizer(raw_session, self.__configuration).remove_invalid_transactions()
        # Check if we have enough transactions
        if len(raw_session.transactions) < self.__configuration.min_transactions_per_session:
            logging.warning("Session %s rejected: not enough transactions (%i)",
                            session_id, len(raw_session.transactions))
            return
        
        # If we are in monitoring window, send attack risk label to monitoring system
        if self.__system_mode_tracker.is_session_in_monitoring_window(session_id):
            self.__communication_controller\
                .send_attack_risk_label(session_id, raw_session.attack_risk_label)
        # Send raw session to preparation system
        self.__communication_controller.send_raw_session(raw_session)
        # Unregister session from system mode tracker
        self.__system_mode_tracker.unregister_session(session_id)
