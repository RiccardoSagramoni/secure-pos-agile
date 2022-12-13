import os

import requests

from utility import get_project_folder

if __name__ == "__main__":
    # Success
    with open(os.path.join(get_project_folder(), 'pytest.ini')) as file:
        r = requests.post("http://127.0.0.1:8000", files={'file': file})
        print(r)
        print(r.text)
    
    # Failure
    r = requests.post("http://127.0.0.1:8000")
    print(r)
    print(r.text)
