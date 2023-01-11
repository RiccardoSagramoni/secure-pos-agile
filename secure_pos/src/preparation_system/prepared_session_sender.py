import logging

import requests


class PreparedSessionSender:

    def __init__(self, url):
        self.url = url

    def send_prepared_session(self, prepared_session_dict):
        try:
            response = requests.post(self.url, json=prepared_session_dict)
            if not response.ok:
                logging.error("Failed to send prepared session:\n%s", prepared_session_dict)
        except requests.exceptions.RequestException as ex:
            logging.error("Unable to send prepared session")
