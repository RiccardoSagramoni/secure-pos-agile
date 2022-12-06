import os
import pandas as pd
import sqlite3


class DBManager:

    def __init__(self, path_db: str):
        self.path_db = path_db

    def create_table(self, query: str) -> None:
        with sqlite3.connect(self.path_db) as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            conn.commit()

    def insert(self, dataframe: pd.DataFrame, table: str) -> bool:
        with sqlite3.connect(self.path_db, timeout=15) as conn:
            res = dataframe.to_sql(table, conn, if_exists="append", index=False)
            return bool(res)

    def read_sql(self, query: str):
        try:
            with sqlite3.connect(self.path_db, timeout=15) as conn:
                return pd.read_sql(query, conn)
        except:
            print("Query exception")
            return None

    def update(self, query: str) -> bool:
        try:
            with sqlite3.connect(self.path_db) as conn:
                cur = conn.cursor()
                cur.execute(query)
                conn.commit()
                return True
        except:
            print("Query exception")
            return False

    def delete_table(self, table: str) -> None:
        with sqlite3.connect(self.path_db) as conn:
            cursor = conn.cursor()
            cursor.execute("DROP TABLE IF EXISTS " + table)
            conn.commit()

    def drop_database(self) -> None:
        os.remove(self.path_db)
