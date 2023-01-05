import sys
from SegregationSystem.Classes import ApplicationController


def main():
    controller = ApplicationController.ApplicationController()
    controller.server_start()
    sys.exit(0)


if __name__ == "__main__":
    main()
