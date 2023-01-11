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
        self.__deployment_classifier = ExecutionSystemDeployment()
        self.__attack_risk_classifier = AttackRiskClassifier()

    def run(self):
        # Start REST server
        self.__communication_controller.start_execution_rest_server()

    def handle_classifier_model_deployment(self) -> None:
        # Start classifier
        self.__deployment_classifier.load_classifier_model()
        self.__system_mode_tracker.development_mode = False

    def handle_new_prepared_session_reception(self, json_session: dict) -> None:
        # Classify session
        session_id = json_session['session_id']
        if not self.__system_mode_tracker.development_mode:
            prepared_session = pd.DataFrame(data=json_session)
            session_risk_level = self.__attack_risk_classifier.provide_attack_risk_level(
                self.__deployment_classifier.get_classifier_model(),
                prepared_session
            )
            if self.__system_mode_tracker.is_session_in_monitoring_window():
                self.__communication_controller.send_attack_risk_label(
                    self.__attack_risk_classifier.attack_risk_label_converter(session_id))

            if session_risk_level > 0:
                print("Attack detected")
