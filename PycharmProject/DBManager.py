import sqlite3
import pandas as pd


class DBManager:

    def __init__(self):
        pass

    @staticmethod
    def insert_record(self, dataframe, path_db, table):
        conn = sqlite3.connect(path_db, timeout=15)
        dataframe.to_sql(table, conn, if_exist="append", index=False)

    @staticmethod
    def execute_query(self):
        pass

    @staticmethod
    def delete_table(self):
        pass

    @staticmethod
    def create_table(self):
        pass

    @staticmethod
    def update_table(self):
        pass

