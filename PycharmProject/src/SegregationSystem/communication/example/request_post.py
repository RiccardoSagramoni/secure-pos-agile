import os

import requests
import json

from utility import get_project_folder

if __name__ == "__main__":
    # Success
    with open(os.path.join(get_project_folder(), 'pytest.ini'), 'rb') as file:
        r = requests.post("http://127.0.0.1:8000/send_file", files={'file': file})
        print(r)
        print(r.text)

    # Failure
    r = requests.post("http://127.0.0.1:8000")
    print(r)
    print(r.text)

    # Success
    content = {"result": "sent and saved"}
    r = requests.post("http://127.0.0.1:8000/send_json", json=content)
    print(r)
    print(r.text)