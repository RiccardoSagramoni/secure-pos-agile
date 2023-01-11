import pandas as pd

from execution_system.execution_configuration import ExecutionConfiguration
from execution_system.communication_controller import CommunicationController
from execution_system.system_mode_tracker import SystemModeTracker
from execution_system.execution_system_deployment import ExecutionSystemDeployment
from execution_system.attack_risk_classifier import AttackRiskClassifier

CONFIGURATION_FILE = 'execution_system/execution_config.json'
CONFIGURATION_SCHEMA = 'execution_system/execution_config_schema.json'


class ExecutionSystemController:

    def __init__(self):
        self.__configuration = ExecutionConfiguration(CONFIGURATION_FILE, CONFIGURATION_SCHEMA)
        self.__communication_controller = \
            CommunicationController(self.__configuration,
                                    self.handle_new_prepared_session_reception,
                                    self.handle_classifier_model_deployment)
        self.__system_mode_tracker = SystemModeTracker(self.__configuration)
        self.__deployed_classifier_model = DeployedClassifierModel()

    def run(self):
        # Start REST server
        self.__communication_controller.start_execution_rest_server()

    def handle_classifier_model_deployment(self) -> None:
        # Start classifier
        self.__deployment_classifier.load_classifier_model()
        self.__system_mode_tracker.development_mode = False

    def handle_new_prepared_session_reception(self, json_session: dict) -> None:
        if self.__system_mode_tracker.development_mode:
            return

        # Get prepared session
        session_id = json_session['session_id']
        prepared_session = pd.DataFrame(data=json_session)

        # Classify session
        attack_risk_classifier = \
            AttackRiskClassifier(self.__deployed_classifier_model.get_classifier_model(),
                                 session_id, prepared_session)
        session_risk_level = attack_risk_classifier.provide_attack_risk_level()

        # Send label to monitoring system
        if self.__system_mode_tracker.is_session_in_monitoring_window():
            self.__communication_controller.send_attack_risk_label(
                attack_risk_classifier.attack_risk_label_converter()
            )

        if session_risk_level > 0:
            print("Attack detected")
