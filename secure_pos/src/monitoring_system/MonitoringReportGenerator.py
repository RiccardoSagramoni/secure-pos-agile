from monitoring_system.MonitoringReport import MonitoringReport
import json


class MonitoringReportGenerator:

    count_report = 0
    report = MonitoringReport()
    labels = None

    def __int__(self, labels):
        self.report = MonitoringReport()
        self.labels = labels
        self.count_report = 0

    def generate_report_json(self):
        report_dict = self.report.to_dict()
        with open('./conf/report' + str(self.count_report) + '.json', 'w', encoding="UTF-8") as json_file:
            json.dump(report_dict, json_file)

    def count_conflicting_labels(self):
        pass

    def count_max_consecutive_conflicting_labels(self):
        pass

    def generate_report(self, labels):
        self.count_report += 1
        self.labels = labels
        self.count_conflicting_labels()
        self.count_max_consecutive_conflicting_labels()
        self.generate_report_json()
