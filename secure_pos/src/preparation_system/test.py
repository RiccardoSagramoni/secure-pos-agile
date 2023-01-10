import json
import logging

import requests

if __name__ == "__main__":
    # trasmetto una raw_session al preparation system
    raw_session_path = "../../data/preparation_system/raw_session.json"
    with open(raw_session_path, "r", encoding="UTF-8") as file:
        raw_session_dict = json.load(file)
    response = requests.post("http://127.0.0.1:8000/", json=raw_session_dict)
    if not response.ok:
        logging.error("Failed to send prepared session:\n%s", raw_session_dict)
