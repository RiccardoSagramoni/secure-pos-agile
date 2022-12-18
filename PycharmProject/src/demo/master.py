import sys
import threading
from time import sleep

from communication import RestServer
from communication.api.file import ReceiveFileApi
from demo import post_resource

semaphore = threading.Semaphore(0)


def handle_last_message() -> None:
    # Notify that the message from last slave has arrived
    semaphore.release()


def start_master_server() -> None:
    # Instantiate server
    server = RestServer()
    server.api.add_resource(ReceiveFileApi,
                            "/",
                            resource_class_kwargs={
                                'filename': 'file.txt',
                                'handler': handle_last_message
                            })
    server.run()


def main(url_slave: str) -> None:
    # Start Flask server as a daemon thread (it dies when main thread dies)
    flask_thread = threading.Thread(target=start_master_server, daemon=True)
    flask_thread.start()
    
    # Send POST request to first slave
    print(f"Send POST request to slave {url_slave}")
    post_resource(url_slave, 'requirements.txt')
    
    # Wait for last message
    semaphore.acquire()
    print('Last message arrived!')
    sleep(1)
    sys.exit(0)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Errore! Serve indirizzo ip del primo nodo")
        sys.exit(1)
    
    main(sys.argv[1])
