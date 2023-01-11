import os
import sys

from developing_system.DevelopingSystemController import DevelopingSystemController

def main():
    controller = DevelopingSystemController()
    controller.run()
    # controller.identify_the_top_mlp_classifiers()
    sys.exit()

if __name__ == "__main__":
    main()

