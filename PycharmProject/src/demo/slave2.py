import sys

from communication import RestServer
from communication.api.file import ReceiveFileApi
from demo import post_resource


def start_slave2_server(next_node):
    filename = 'file.txt'
    
    # Instantiate server
    server = RestServer()
    server.api.add_resource(ReceiveFileApi,
                            "/",
                            resource_class_kwargs={
                                'filename': filename,
                                # l'handler manda la richiesta POST al master
                                'handler': lambda: post_resource(next_node, filename)
                            })
    server.run(debug=True)


def main(next_node):
    # start server and attend post request from slave2
    start_slave2_server(next_node)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Errore! Serve indirizzo ip del master")
        exit(1)

    main(str(sys.argv[1]))
