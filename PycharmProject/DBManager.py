import sqlite3
import pandas as pd


class DBManager:

    def __init__(self):
        pass

    @staticmethod
    def insert_record(dataframe, path_db, table):
        conn = sqlite3.connect(path_db, timeout=15)
        dataframe.to_sql(table, conn, if_exist="append", index=False)

    @staticmethod
    def execute_query(path_db, query):
        conn = sqlite3.connect(path_db)
        try:
            res = pd.read_sql(query, conn)
            conn.commit()
        except:
            print("Exeption in query - special char")
        conn.close()
        return res

    @staticmethod
    def delete_table(path_db, table):
        conn = sqlite3.connect(path_db)
        cursor = conn.cursor()
        cursor.execute("DROP TABLE IF EXISTS " + table)
        conn.commit()
        conn.close()

    @staticmethod
    def create_table(self, path_db, query):
        conn = sqlite3.connect(path_db)
        cursor = conn.cursor()
        cursor.execute(query)
        conn.commit()
        conn.close()

    @staticmethod
    def update_table(self, path_db, query):
        conn = sqlite3.connect(path_db)
        try:
            cur = conn.cursor()
            cur.execute(query)
            conn.commit()
        except:
            print("Query exception")
        conn.close()



