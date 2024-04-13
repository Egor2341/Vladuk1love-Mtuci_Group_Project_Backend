# from main import client
#
# def test_get():
#     res = client.get('/smth')
#     assert res.status_code == 200
#
#     assert res.get_json()[0]['id'] == 1


# import os
# import requests
#
# photo = "D:\wall\e8738644ceea3c8a3d29a798e71004d9.jpg"
# files = {
#     'file': (os.path.basename(photo), open(photo, 'rb'), 'application/octet-stream')
# }
# res = requests.post('http://127.0.0.1:5000/photos/Egorik', files=files)
# print(res.text)

# import requests
#
# res = requests.post('http://127.0.0.1:5000/registration', json={
#     'login': 'Egorik22',
#     'name': 'Egor',
#     'age': 18,
#     'sex': 'male',
#     'password': 'qwerty'
# })
#
# print(res.text)

# from s3 import s3
# # photo = "D:\wall\e8738644ceea3c8a3d29a798e71004d9.jpg"
# photo = 'D:\PycharmProjects\Backend_Egor\photos\w1.jpg'
# with open(photo, 'wb') as data:
#     s3.download_file(data, '1')

import requests

res = requests.post('http://127.0.0.1:5000/login', json={
    'login': 'Egorik22',
    'password': 'qwerty'
})

print(res.text)