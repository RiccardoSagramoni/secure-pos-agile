from database.DBManager import DBManager
import pandas as pd
import pytest

path_db = "test.db"
test_data = {
    "ex_id": "1",
    "name": "team",
    "lastName": "Cammeo"
}
new_test_data = {
    "ex_id": "1",
    "name": "pippo",
    "lastName": "Cammeo"
}
test_dataframe = pd.DataFrame(test_data, index=[0])
new_test_dataframe = pd.DataFrame(new_test_data, index=[0])


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
    except Exception:
        assert False


def test_insert(db):
    assert db.insert(test_dataframe, "example")


def test_read_sql(db):
    try:
        query = "SELECT * FROM example WHERE ex_id='1'"
        result = db.read_sql(query)
        assert result.equals(test_dataframe)
    except Exception:
        assert False


def test_update(db):
    try:
        assert db.update("UPDATE example SET name='pippo' WHERE ex_id='1'")
        
        result = db.read_sql("SELECT * FROM example WHERE ex_id='1'")
        assert result.equals(new_test_dataframe)
    except Exception:
        assert False


def test_delete_table(db):
    try:
        db.delete_table(table="example")
        assert True
    except Exception:
        assert False
