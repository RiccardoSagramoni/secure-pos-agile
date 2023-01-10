import json
import jsons
import os
import utility

REPORT_TOP_CLASSIFIERS_PATH = 'development_system/reports/report_top_classifiers.json'

class TopClassifierReportGenerator:

    def __init__(self, grid_search):

        self.grid_search = grid_search

    def generate_report(self):

        report = {
            'report_title:': 'Report of the Top Classifiers',
            'validation_tolerance': self.grid_search.validation_tolerance,
            'number_of_top_classifiers': self.grid_search.number_of_top_classifiers,
            'top_classifiers': []
        }

        for classifier in self.grid_search.top_classifiers_object_list:
            report['top_classifiers'].append(jsons.dump(classifier))

        with open(os.path.join(utility.data_folder, REPORT_TOP_CLASSIFIERS_PATH), 'w') as report_file:
            report_file.write(json.dumps(report, indent=2))