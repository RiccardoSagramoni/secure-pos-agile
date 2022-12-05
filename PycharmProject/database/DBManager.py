import sqlite3
import pandas as pd


class DBManager:

    def __init__(self, path_db):
        self.path_db = path_db

    def create_table(self, query):
        conn = sqlite3.connect(self.path_db)
        cursor = conn.cursor()
        cursor.execute(query)
        conn.commit()
        conn.close()

    def insert_record(self, dataframe, table):
        conn = sqlite3.connect(self.path_db, timeout=15)
        res = dataframe.to_sql(table, conn, if_exists="append", index=False)
        return bool(res)

    def execute_query(self, query):
        conn = sqlite3.connect(self.path_db)
        try:
            res = pd.read_sql(query, conn)
            conn.commit()
        except:
            res = None
            print("Query exception")
        conn.close()
        return res

    def update_table(self, query):
        conn = sqlite3.connect(self.path_db)
        try:
            cur = conn.cursor()
            cur.execute(query)
            conn.commit()
        except:
            print("Query exception")
        conn.close()

    def delete_table(self, table):
        conn = sqlite3.connect(self.path_db)
        cursor = conn.cursor()
        cursor.execute("DROP TABLE IF EXISTS " + table)
        conn.commit()
        conn.close()
