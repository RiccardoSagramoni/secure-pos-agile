from demo import get_resource, IP_MASTER, post_resource


def main():

    # Receive hello message
    print("Get hello resource")
    get_resource(IP_MASTER + "/Hello", None)

    print("Get hello with post")
    sent_json = {"name": "hello master"}
    post_resource(IP_MASTER + "/Hello", sent_json)

    # Receive json file
    print("Get json resource")
    get_resource(IP_MASTER + "/json/example.json", None)

    # Send json file
    print("Send json resource")
    sent_json = {"test_post1": "rest_api"}
    post_resource(IP_MASTER + "/json/example.json", sent_json)


if __name__ == "__main__":
    main()