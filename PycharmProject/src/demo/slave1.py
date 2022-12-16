import sys

from communication import RestServer
from communication.api.file import ReceiveFileApi
from demo import post_resource


def start_slave1_server(next_node):
    # Instantiate server
    server = RestServer()
    server.api.add_resource(ReceiveFileApi,
                            "/",
                            resource_class_kwargs={'filename': 'file.txt',
                                                   # l'handler manda la richiesta POST al prossimo slave
                                                   'handler': post_resource(next_node, "file.txt")
                                                   })
    server.run(debug=True)


def main(next_node):
    # run server and attend post request from master
    start_slave1_server(next_node)


if __name__ == "__main__":

    if len(sys.argv) < 2:
        print("Errore! Serve indirizzo ip del prossimo slave")
        exit(1)

    main(str(sys.argv[1]))
