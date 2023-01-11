import sys

from developing_system.DevelopingSystemController import DevelopingSystemController

def main():
    controller = DevelopingSystemController()
    controller.identify_the_top_mlp_classifiers()
    sys.exit(0)

if __name__ == "__main__":
    main()

