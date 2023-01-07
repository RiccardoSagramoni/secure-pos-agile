import threading

from communication import RestServer
from communication.api.json_transfer import ReceiveJsonApi
from ingestion_system.configuration import Configuration
from ingestion_system.record_synchronizer import RecordSynchronizer


class CommunicationController:
    
    def __init__(self,
                 conf: Configuration,
                 record_sync: RecordSynchronizer):
        self.configuration = conf
        self.record_synchronizer = record_sync
    
    def handle_message(self, json_record: dict) -> None:
        """
        Start a new thread which stores the received record.
        :param json_record: data received from a client-side system.
        """
        threading.Thread(
            target=self.record_synchronizer.handle_new_record_reception,
            args=json_record
        ).start()
    
    def start_ingestion_rest_server(self) -> None:
        server = RestServer()
        server.api.add_resource(ReceiveJsonApi,
                                "/",
                                resource_class_kwargs={
                                    'handler': lambda x: self.handle_message(x)
                                })
        server.run(debug=True)
