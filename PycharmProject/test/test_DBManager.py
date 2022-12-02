from database import DBManager

db = DBManager.DBManager()


def test_create_table():
    try:
        path_db = "test.db"
        query = "CREATE TABLE exemple (ex_id TEXT PRIMARY KEY, name TEXT, lastName TEXT)"
        db.create_table(path_db, query)
        assert True
    except:
        assert False


def test_insert_record():
    assert False


def test_execute_query():
    assert False


def test_update_table():
    assert False


def test_delete_table():
    assert False
