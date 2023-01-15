import logging

from database import DatabaseConnector


class LabelStorer:

    def __init__(self):
        self.db = DatabaseConnector('monitoringDB.db')

    def store_label(self, label, table):
        if not self.db.insert(label, table):
            logging.error("Impossible to store the label")
            raise ValueError("Monitoring System label storage failed")

    def create_table(self, query):
        self.db.create_table(query)

    def delete_all_labels(self, query):
        self.db.update(query)

    def select_label(self, query):
        return self.db.read_sql(query)
