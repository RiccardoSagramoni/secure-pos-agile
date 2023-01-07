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


if __name__ == "__main__":
    test = LabelStorer()
    labels = test.select_label("SELECT ex.session_id, ex.value as expertValue, cl.value as classifierValue "
                               "FROM expertLabel AS ex JOIN classifierLabel AS cl ON ex.session_id = cl.session_id")
    print(labels)

    for row in labels.index:
        print("id:" + labels["session_id"][row])
        print(labels["expertValue"][row])
