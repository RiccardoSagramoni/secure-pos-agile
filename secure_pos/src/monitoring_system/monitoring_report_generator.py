from monitoring_system.monitoring_report import MonitoringReport
import json


class MonitoringReportGenerator:

    def __init__(self, labels):
        self.report = MonitoringReport()
        self.labels = labels
        self.count_report = 0

    def generate_report_json(self):
        report_dict = self.report.to_dict()
        with open('./conf/report' + str(self.count_report) + '.json', 'w', encoding="UTF-8") as json_file:
            json.dump(report_dict, json_file)

    def count_conflicting_labels(self):
        count = 0
        for row in self.labels.index:
            expert_label = self.labels["expertValue"][row]
            classifier_label = self.labels["classifierValue"][row]
            if expert_label != classifier_label:
                count += 1
        self.report.conflicting_labels = count

    def count_max_consecutive_conflicting_labels(self):
        pass

    def generate_report(self):
        self.count_report += 1

        # conto il numero di label discordanti
        self.count_conflicting_labels()

        # conto il numero massimo di label consecutive discordanti
        self.count_max_consecutive_conflicting_labels()

        # genero il file json contente il report
        self.generate_report_json()
