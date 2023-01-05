from monitoring_system.MonitoringReport import MonitoringReport
import json


class MonitoringReportGenerator:

    report = MonitoringReport()

    def generate_report(self):
        report_dict = self.report.to_dict()
        with open('./conf/report.json', 'w') as json_file:
            json.dump(report_dict, json_file)

    def count_conflicting_labels(self):
        pass

    def count_max_consecutive_conflicting_labels(self):
        pass
