import os
import sys
import threading

from flask import request

from communication import RestServer
from communication.api.file import ReceiveFileApi
from demo import post_resource


def shutdown_server():
    print('ciao ciao2')
    sys.exit(0)
    # func = request.environ.get('werkzeug.server.shutdown')
    # if func is None:
    #     raise RuntimeError('Not running with the Werkzeug Server')
    # func()

def start_master_server():
    # Instantiate server
    server = RestServer()
    server.api.add_resource(ReceiveFileApi,
                            "/",
                            resource_class_kwargs={
                                'filename': 'file.txt',
                                'handler': shutdown_server()
                            })
    server.run(debug=True)


def main(next_node):
    print('ciao')
    # start a thread with start_master_server
    master_thread = threading.Thread(target=start_master_server())
    master_thread.start()

    # Send POST request to first slave
    post_resource(next_node, 'requirements.txt')

    # Wait for last message
    master_thread.join()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Errore! Serve indirizzo ip del primo nodo")
        sys.exit(1)

    main(str(sys.argv[1]))
