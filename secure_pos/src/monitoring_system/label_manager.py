import threading

import pandas as pd

from monitoring_system.label import Label
from monitoring_system.label_storer import LabelStorer
from monitoring_system.monitoring_report_generator import MonitoringReportGenerator


class LabelManager:

    def __init__(self):
        self.tot_labels_from_expert = 0
        self.tot_labels_from_classifier = 0
        self.storer = LabelStorer()
        self.access_to_db = threading.Semaphore(1)

    def count_labels(self, source):
        if source == 'classifier':
            self.tot_labels_from_classifier += 1
        else:
            self.tot_labels_from_expert += 1

    def store_label(self, monitoring_window_length, label):
        # blocco l'accesso al db
        self.access_to_db.acquire()
        session_id = label["session_id"]
        source = label["source"]
        value = label["value"]
        label = Label(session_id, value, source)
        label_dataframe = pd.DataFrame(label.to_dict(), index=[0], columns=["session_id", "value"])
        if label.source == 'classifier':
            self.count_labels('classifier')
            self.storer.store_label(label_dataframe, 'classifierLabel')
        else:
            self.count_labels('expert')
            self.storer.store_label(label_dataframe, 'expertLabel')
        if self.tot_labels_from_expert == monitoring_window_length or \
                self.tot_labels_from_classifier == monitoring_window_length:

            # carico le label in memoria
            query = "SELECT ex.session_id, ex.value as expertValue, " \
                    "cl.value as classifierValue " \
                    "FROM expertLabel AS ex " \
                    "JOIN classifierLabel AS cl ON ex.session_id = cl.session_id"
            labels = self.storer.select_label(query)

            # le elimino dal db
            query = "DELETE FROM classifierLabel"
            self.storer.delete_all_labels(query)
            query = "DELETE FROM expertLabel"
            self.storer.delete_all_labels(query)

            # avvio il thread per produrre il report di monitoraggio
            report = MonitoringReportGenerator(labels)
            thread = threading.Thread(target=report.generate_report)
            thread.start()

        self.access_to_db.release()
