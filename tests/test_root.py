def test_conn(client):
    assert client.get('/').status_code == 200
