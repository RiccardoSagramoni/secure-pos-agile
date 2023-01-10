import logging

import requests


def send_label(label_json):
    response = requests.post("http://127.0.0.1:8000/", json=label_json)
    if not response.ok:
        logging.error("Failed to send label:\n%s", label_json)


if __name__ == "__main__":
    for i in range(5):
        # trasmetto una label al monitoring system
        label = {
            "session_id": str(i),
            "source": "expert",
            "value": "attack"
        }
        send_label(label)
        label = {
            "session_id": str(i),
            "source": "classifier",
            "value": "normal"
        }
        send_label(label)

    for i in range(5, 10):
        # trasmetto una label al monitoring system
        label = {
            "session_id": str(i),
            "source": "expert",
            "value": "attack"
        }
        send_label(label)
        label = {
            "session_id": str(i),
            "source": "classifier",
            "value": "attack"
        }
        send_label(label)

    for i in range(10, 18):
        # trasmetto una label al monitoring system
        label = {
            "session_id": str(i),
            "source": "expert",
            "value": "normal"
        }
        send_label(label)
        label = {
            "session_id": str(i),
            "source": "classifier",
            "value": "attack"
        }
        send_label(label)

    for i in range(18, 30):
        # trasmetto una label al monitoring system
        label = {
            "session_id": str(i),
            "source": "expert",
            "value": "normal"
        }
        send_label(label)
        label = {
            "session_id": str(i),
            "source": "classifier",
            "value": "normal"
        }
        send_label(label)
