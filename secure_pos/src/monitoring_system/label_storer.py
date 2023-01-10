import logging

from database.DBManager import DBManager


class LabelStorer:

    def __init__(self):
        self.db = DBManager('monitoringDB.db')

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


if __name__ == "__main__":
    test = LabelStorer()
    test.delete_all_labels("DELETE FROM classifierLabel")
    test.delete_all_labels("DELETE FROM expertLabel")
    test1 = test.select_label("SELECT * FROM classifierLabel")
    print(test1)
    test2 = test.select_label("SELECT * FROM expertLabel")
    print(test2)
