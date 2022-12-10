import requests

IP_MASTER = "http://127.0.0.1:8000"


def print_result(response):
    print("Status_code: " + str(response.status_code))
    print(response.text)


def get_resource(url, sent_json):
    if sent_json:
        response = requests.get(url, json=sent_json)
    else:
        response = requests.get(url)
    print_result(response)


def post_resource(url, sent_json):
    response = requests.post(url, json=sent_json)
    print_result(response)
