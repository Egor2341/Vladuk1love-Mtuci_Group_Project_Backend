# from main import client
#
# def test_get():
#     res = client.get('/smth')
#     assert res.status_code == 200
#
#     assert res.get_json()[0]['id'] == 1
import json
import os

import requests

photo = "D:\wall\d173a9ec35f0e6b34391ebc23452724f.jpg"
login = {'login': 'Bob_Bob'}
files = {
    'file': (os.path.basename(photo), open(photo, 'rb'), 'application/octet-stream')
}
data = {'name': 'login', 'data': json.dumps(login)}
res = requests.post('http://127.0.0.1:5000/photos', files=files, data=data)
# res = requests.post('http://127.0.0.1:5000/registration', json={
#     'name': 'Bob',
#     'login': 'Bob_Bob',
#     'age': 18,
#     'sex': 'male',
#     'password': 'qwerty'
# })
print(res.text)
