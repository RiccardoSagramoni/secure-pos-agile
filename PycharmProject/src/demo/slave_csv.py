from demo import get_resource, IP_MASTER

def main():
    # Receive hello message
    print("Get hello resource")
    get_resource(IP_MASTER + "/Hello", None)

    # Receive csv file
    print("Get csv resource")
    get_resource(IP_MASTER + "/csv/commercial.csv", None)


if __name__ == "__main__":
    main()