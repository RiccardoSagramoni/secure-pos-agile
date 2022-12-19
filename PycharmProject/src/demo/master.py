import sys
import threading
from time import sleep

from communication import RestServer
from communication.api.file import ReceiveFileApi
from demo import post_resource

# This semaphore notifies the main thread when
# the last message of the toolchain has been received
message_received = threading.Semaphore(0)


def handle_last_message() -> None:
    # Notify that the message from last slave has arrived
    message_received.release()


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
    message_received.acquire()
    print('Last message arrived!')
    # Allows Flask application to return correct status code before terminating
    sleep(1)
    sys.exit(0)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Errore! Serve url del primo nodo (formato http://<ip>:<port>)")
        sys.exit(1)
    
    main(sys.argv[1])
