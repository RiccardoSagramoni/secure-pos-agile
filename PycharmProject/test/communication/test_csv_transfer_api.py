from conftest import GET_CSV_URL, GET_CSV_DIR_URL


def test_get_csv__get(client):
    response = client.get(GET_CSV_URL)
    assert response.status_code == 200


def test_get_csv_inside_directory__get(client):
    response = client.get(GET_CSV_DIR_URL + '/commercial.csv')
    assert response.status_code == 200


def test_get_csv_inside_directory__wrong_csv_file(client):
    response = client.get(GET_CSV_DIR_URL + '/wrong.file')
    assert response.status_code == 404
