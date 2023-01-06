import os
import threading

import pandas as pd

from monitoring_system.Label import Label
from monitoring_system.LabelStorer import LabelStorer
from utility import get_received_data_folder


class LabelManager:

    tot_labels_from_classifier = 0
    tot_labels_from_expert = 0
    storer = LabelStorer()
    access_to_db = threading.Semaphore(1)
    pathLabel = os.path.join(get_received_data_folder(), 'label.json')

    def __int__(self, tot_labels_from_classifier, tot_labels_from_expert):
        self.tot_labels_from_expert = tot_labels_from_expert
        self.tot_labels_from_classifier = tot_labels_from_classifier

    def count_labels(self, from_where):
        if from_where == 'classifier':
            self.tot_labels_from_classifier += 1
        else:
            self.tot_labels_from_expert += 1

    def store_label(self, monitoring_window_length):
        # blocco l'accesso al db
        self.access_to_db.acquire()
        label = Label()
        label.load_from_file(self.pathLabel)
        label_dataframe = pd.DataFrame(label.to_dict(), index=[0])
        if label.source == 'classifier':
            self.count_labels('classifier')
            self.storer.store_label(label_dataframe, 'classifierLabel')
        else:
            self.count_labels('expert')
            self.storer.store_label(label_dataframe, 'expertLabel')
        if self.tot_labels_from_expert == monitoring_window_length or \
                self.tot_labels_from_classifier == monitoring_window_length:
            # avvio il monitoraggio su un altro thread
            # in questo modo posso continuare a memorizzare label per il report successivo

            # prima di procedere con il report
            # caricare le etichette in memoria
            # eliminarle dal db
            # avviare il thread per il monitoraggio

            pass
        self.access_to_db.release()
