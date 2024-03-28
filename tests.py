# from main import client
#
# def test_get():
#     res = client.get('/smth')
#     assert res.status_code == 200
#
#     assert res.get_json()[0]['id'] == 1

import requests

res = requests.get('http://127.0.0.1:5000/profile', json={
    'login': 'Bob_52'
})
print(res.json())

