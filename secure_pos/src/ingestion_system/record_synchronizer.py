import logging

from ingestion_system.database_controller import DatabaseController


class RecordSynchronizer:
    
    def __init__(self,
                 db_controller: DatabaseController):
        self.database_controller = db_controller
    
    def __parse_json_record(self, json_record):
        pass
    
    def handle_new_record_reception(self, json_records: dict):
        # TODO validate json document??
        
        # Insert records in database
        ret = self.database_controller.insert_transaction_record(json_records)
        if not ret:
            logging.error(f"Impossible to insert records in db: {json_records}")
            return
        
        # Check if we have all the necessary data of the session
        session_id = json_records['id']
        session_completed = self.database_controller.check_if_session_is_completed(session_id)
        if not session_completed:
            return
        
        # Synchronize samples
        session = self.synchronize_session(json_records['id'])
        return
    
    def synchronize_session(self, session_id: str):
        pass
