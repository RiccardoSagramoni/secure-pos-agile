import logging

import requests

if __name__ == "__main__":
    # trasmetto una label al monitoring system
    label = {

    }
    response = requests.post("http://127.0.0.1:8000/", json=label)
    if not response.ok:
        logging.error("Failed to send prepared session:\n%s", label)
