from database.DBManager import DBManager


class LabelStorer:

    def __init__(self):
        self.db = DBManager('monitoringDB.db')

    def store_label(self, label, table):
        self.db.insert(label, table)

    def create_table(self, query):
        self.db.create_table(query)

    def delete_all_labels(self, query):
        self.db.update(query)

    def select_label(self, query):
        return self.db.read_sql(query)
