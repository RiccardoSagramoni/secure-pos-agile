from demo import get_resource, IP_MASTER


def main():
    # Receive hello message
    print("Get hello resource")
    get_resource(IP_MASTER + "/Hello", None)

    # Receive json file
    print("Get json resource")
    get_resource(IP_MASTER + "/file/example.json", None)


if __name__ == "__main__":
    main()
