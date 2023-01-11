import logging

import requests


class PreparedSessionSender:

    def __init__(self, url):
        self.url = url

    def send_prepared_session(self, prepared_session_dict):
        response = requests.post(self.url, json=prepared_session_dict)
        if not response.ok:
            logging.error("Failed to send prepared session:\n%s", prepared_session_dict)
