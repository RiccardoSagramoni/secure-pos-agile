from database import DBManager
import pandas as pd

db = DBManager.DBManager()
path_db = "test.db"


def test_create_table():
    try:
        query = "CREATE TABLE example (ex_id TEXT PRIMARY KEY, name TEXT, lastName TEXT)"
        db.create_table(path_db, query)
        assert True
    except:
        assert False


def test_insert_record():
    data = {"ex_id": "1",
            "name": "team",
            "lastName": "cammeo"}
    df = pd.DataFrame(data, index=[0])
    try:
        db.insert_record(df, path_db, "example")
        assert True
    except:
        assert False


def test_execute_query():
    assert False


def test_update_table():
    assert False


def test_delete_table():
    assert False
