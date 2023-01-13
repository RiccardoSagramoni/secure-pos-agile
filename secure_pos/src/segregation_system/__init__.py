import sys

from segregation_system.objects.segregation_system_controller import SegregationSystemController


def main():
    controller = SegregationSystemController()
    controller.check_response()
    sys.exit(0)


if __name__ == "__main__":
    main()
