def test_conn(client):
    assert client.get('/').status_code == 200

def test_log(client):
    assert client.get('/login/').status_code == 200

def test_sign(client):
    assert client.get('/signup/').status_code == 200

#def test_index(client):
#    assert client.get('/index/').status_code == 200

def test_flat(client):
    assert client.get('/flat/').status_code == 200

#def test_logout(client):
#    assert client.get('/logout/').status_code == 200
