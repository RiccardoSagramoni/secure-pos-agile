import os
import sys

from development_system.development_system_controller import DevelopmentSystemController

def main():
    controller = DevelopmentSystemController()
    controller.run()
    # controller.execution_control_of_the_development_system()
    sys.exit()

if __name__ == "__main__":
    main()

