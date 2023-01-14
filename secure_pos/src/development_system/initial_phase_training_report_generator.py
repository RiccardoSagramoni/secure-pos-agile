import json
import os
import utility

REPORT_INITIAL_PHASE_TRAINING_PATH = 'development_system/reports/initial_phase/report_initial_phase_training.json'

class InitialPhaseTrainingReportGenerator:

    @staticmethod
    def generate_report(self, training_error, validation_error, hyper_parameters):
        report = {
            'report_title:': 'Report of the Initial Phase Training',
            'hyper_parameters': hyper_parameters,
            'training_error': training_error,
            'validation_error': validation_error
        }

        with open(os.path.join(utility.data_folder, REPORT_INITIAL_PHASE_TRAINING_PATH), 'w') as report_file:
            report_file.write(json.dumps(report, indent=2))