import os
import sqlite3
import pandas as pd



class DBManager:  # todo change name to database_connector.DatabaseConnector
    """
    Class responsible to handle the "low level" accesses to the database.
    """
    
    def __init__(self, db_path: str):
        self.__database_path = db_path
    
    def __execute_commit_query(self, query: str):
        with sqlite3.connect(self.__database_path) as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            conn.commit()
    
    def create_table(self, query: str):
        self.__execute_commit_query(query)
    
    def insert(self, dataframe: pd.DataFrame, table: str) -> bool:
        with sqlite3.connect(self.__database_path, timeout=15) as conn:
            res = dataframe.to_sql(table, conn, if_exists="append", index=False)
            return bool(res)
    
    def read_sql(self, query: str):
        with sqlite3.connect(self.__database_path, timeout=15) as conn:
            return pd.read_sql(query, conn)
    
    def update(self, query: str) -> None:
        self.__execute_commit_query(query)
    
    def delete_table(self, table: str) -> None:
        self.__execute_commit_query(f"DROP TABLE IF EXISTS {table};")
    
    def drop_database(self) -> None:
        try:
            os.remove(self.__database_path)
        except FileNotFoundError:
            return
