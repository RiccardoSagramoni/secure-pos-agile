import json
import jsons
import os
import utility

REPORT_TOP_CLASSIFIERS_PATH = 'development_system/reports/top_classifiers/report_top_classifiers.json'

class TopClassifierReportGenerator:

    def generate_report(self, grid_search):

        report = {
            'report_title:': 'Report of the Top Classifiers',
            'validation_tolerance': grid_search.validation_tolerance,
            'number_of_top_classifiers': grid_search.number_of_top_classifiers,
            'top_classifiers': []
        }

        for classifier in grid_search.top_classifiers_object_list:
            report['top_classifiers'].append(jsons.dump(classifier))

        with open(os.path.join(utility.data_folder, REPORT_TOP_CLASSIFIERS_PATH), 'w') as report_file:
            report_file.write(json.dumps(report, indent=2))