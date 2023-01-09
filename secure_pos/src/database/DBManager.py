import os
import sqlite3
import pandas as pd


class DBManager:

    def __init__(self, path_db: str):
        self.path_db = path_db
    
    def __execute_commit_query(self, query: str):
        with sqlite3.connect(self.path_db) as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            conn.commit()
    
    def create_table(self, query: str):
        self.__execute_commit_query(query)

    def insert(self, dataframe: pd.DataFrame, table: str) -> bool:
        with sqlite3.connect(self.path_db, timeout=15) as conn:
            res = dataframe.to_sql(table, conn, if_exists="append", index=False)
            return bool(res)
    
    def read_sql(self, query: str):
        try:
            with sqlite3.connect(self.path_db, timeout=15) as conn:
                return pd.read_sql(query, conn)
        except Exception:
            print("Query exception")
            return None

    def update(self, query: str) -> bool:
        try:
            self.__execute_commit_query(query)
            return True
        except Exception:
            print("Query exception")
            return False
    
    def delete_table(self, table: str) -> None:
        with sqlite3.connect(self.path_db) as conn:
            cursor = conn.cursor()
            cursor.execute("DROP TABLE IF EXISTS " + table)
            conn.commit()

    def drop_database(self) -> None:
        os.remove(self.path_db)
