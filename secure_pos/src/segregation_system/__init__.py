import sys
from src.segregation_system.Classes.SegregationSystemController import SegregationSystemController


def main():
    controller = SegregationSystemController()
    controller.server_start()
    sys.exit(0)


if __name__ == "__main__":
    main()
