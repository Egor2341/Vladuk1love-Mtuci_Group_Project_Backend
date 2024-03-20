from app import client

def test_get():
    res = client.get('/smth')
    assert res.status_code == 200

    assert res.get_json()[0]['id'] == 1