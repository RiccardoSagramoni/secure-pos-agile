import json
import jsons
import os
import utility

REPORT_BEST_CLASSIFIER_PATH = 'development_system/reports/best_classifier/report_best_classifier.json'


class TestBestCLassifierReportGenerator:

    @staticmethod
    def generate_report(self, test_tolerance, id_best_classifier, training_error, test_error):

        report = {
            'report_title:': 'Report of the Test of the best classifier',
            'id_best_classifier' : id_best_classifier,
            'test_tolerance': test_tolerance,
            'test_error': test_error,
            'training_error': training_error
        }

        with open(os.path.join(utility.data_folder, REPORT_BEST_CLASSIFIER_PATH), 'w') as report_file:
            report_file.write(json.dumps(report, indent=2))
