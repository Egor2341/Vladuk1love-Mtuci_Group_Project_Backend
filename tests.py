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

import requests

# res = requests.post('http://127.0.0.1:5000/user_preferences', json={
#     'login': 'Egorik222',
#     'age_pref': '18-20',
#     'height_pref': '50-100',
#     'weight_pref': '150-200',
#     'habbits': 'smoking'
# })

res = requests.put('http://127.0.0.1:5000/user_preferences', json={
    'login': 'Egorik222',
    'age_pref': '19-20',
    'height_pref': '150-200',
    'weight_pref': '50-100',
    'habbits': 'no smoking'
})
print(res.json())
# import requests
#
# res = requests.post('http://127.0.0.1:5000/user_info', json={
#     'login': 'Egorik222',
#     'about_me': 'Egorik12',
#     'interests': 'Egor21',
#     'z': 'абракадабра',
#     'height': 'dada',
#     'education': 'fdsfsdfs'
# })
# #
# print(res.json())


# res = requests.get('http://127.0.0.1:5000/user_info/Egorik2242')
# print(res.json())
# from s3 import s3
# # photo = "D:\wall\e8738644ceea3c8a3d29a798e71004d9.jpg"
# photo = 'D:\PycharmProjects\Backend_Egor\photos\w1.jpg'
# with open(photo, 'wb') as data:
#     s3.download_file(data, '1')

# import requests
#
# res = requests.post('http://127.0.0.1:5000/login', json={
#     'login': 'Egorik22',
#     'password': 'qwert2y'
# })
#
# print(res.json())
