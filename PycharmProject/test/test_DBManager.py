from database import DBManager
import pandas as pd

path_db = "test.db"
db = DBManager.DBManager(path_db)


def test_create_table():
    try:
        query = "CREATE TABLE example (ex_id TEXT PRIMARY KEY UNIQUE, name TEXT, lastName TEXT)"
        db.create_table(query)
        assert True
    except:
        assert False


def test_insert_record():
    data = {"ex_id": "1",
            "name": "team",
            "lastName": "Cammeo"}
    df = pd.DataFrame(data, index=[0])
    res = db.insert_record(df, table="example")
    if res:
        assert True
    else:
        assert False


def test_execute_query():
    try:
        query = "SELECT * FROM example"
        res = db.execute_query(query)
        if res is not None:
            print(res)
        else:
            print("empty table")
        assert True
    except:
        assert False


def test_update_table():
    try:
        query = "UPDATE example SET name='pippo' WHERE ex_id='2'"
        db.update_table(query)
        query = "SELECT * FROM example"
        res = db.execute_query(query)
        print(res)
        assert True
    except:
        assert False


def test_delete_table():
    try:
        db.delete_table(table="example")
        assert True
    except:
        assert False
