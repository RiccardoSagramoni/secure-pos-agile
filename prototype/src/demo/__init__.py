import os

import requests

from utility import get_project_folder


def print_result(response):
    print("Status_code: " + str(response.status_code))
    print(response.text)


def post_resource(ip_address, filename):
    with open(os.path.join(get_project_folder(), filename), 'rb') as file:
        response = requests.post(ip_address, files={'file': file})
        print_result(response)
