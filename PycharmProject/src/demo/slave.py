import os
import sys
import threading

from communication import RestServer
from communication.api.file_transfer import ReceiveFileApi
from demo import post_resource
from utility import get_received_data_folder


def handle_message(next_node, filename):
    # When the slave receives a message, generate a new thread
    # which replicates the message to the next node in the toolchain
    thread = threading.Thread(target=post_resource, args=(next_node, os.path.join(get_received_data_folder(), filename)))
    thread.start()


def start_slave_server(next_node):
    # Path where to save the received file
    filename = 'file.txt'
    
    # Instantiate server
    server = RestServer()
    server.api.add_resource(ReceiveFileApi,
                            "/",
                            resource_class_kwargs={
                                'filename': filename,
                                # l'handler manda la richiesta POST al prossimo nodo
                                'handler': lambda: handle_message(next_node, filename)
                            })
    server.run(debug=True)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Errore! Serve indirizzo ip del prossimo nodo")
        sys.exit(1)
    
    start_slave_server(str(sys.argv[1]))
