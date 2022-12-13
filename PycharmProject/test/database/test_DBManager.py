from database.DBManager import DBManager
import pandas as pd
import pytest

path_db = "test.db"


@pytest.fixture(scope='package')
def db():
    db = DBManager(path_db)
    yield db
    db.drop_database()


def test_create_table(db):
    try:
        query = "CREATE TABLE example (ex_id TEXT PRIMARY KEY UNIQUE, name TEXT, lastName TEXT)"
        db.create_table(query)
        assert True
    except:
        assert False


def test_insert(db):
    data = {"ex_id": "1",
            "name": "team",
            "lastName": "Cammeo"}
    df = pd.DataFrame(data, index=[0])
    assert db.insert(df, table="example")


def test_read_sql(db):
    try:
        query = "SELECT * FROM example"
        res = db.read_sql(query)
        if res is not None:
            print(res)
        else:
            print("empty table")
        assert True
    except:
        assert False


def test_update(db):
    try:
        query = "UPDATE example SET name='pippo' WHERE ex_id='2'"
        db.update(query)
        query = "SELECT * FROM example"
        res = db.read_sql(query)
        print(res)
        assert True
    except:
        assert False


def test_delete_table(db):
    try:
        db.delete_table(table="example")
        assert True
    except:
        assert False
