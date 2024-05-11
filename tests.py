# from main import client
#
# def test_get():
#     res = client.get('/smth')
#     assert res.status_code == 200
#
#     assert res.get_json()[0]['id'] == 1


import os
import requests

photo = r"C:\Users\Давид\Downloads\i.jpg"
files = {
    'file': (os.path.basename(photo), open(photo, 'rb'), 'application/octet-stream')
}
res = requests.post('http://127.0.0.1:5000/up_photos/dawud2/img', files=files)
print(res.text)
#
# import requests

# res = requests.put('http://127.0.0.1:5000/user_preferences/Egorik222', json={
#     'age_pref': '18-200',
#     'height_pref': '50-2100',
#     'weight_pref': '150-200',
#     'habbits': 'smoking'
# })

# res = requests.post('http://127.0.0.1:5000/registration', json={
#     'name': "Egor",
#     'login': 'Egorik',
#     'password': '1111',
#     'age': 15,
#     'sex': 'Male'
# })
# print(res.json())

# json = {
#     'age': ['lox', 'pidr', 20]
# }
#
# print(json['age'][0])

# import requests
#
# res = requests.put('http://127.0.0.1:5000/user_info/Egorik222', json={
#     'about_me': 'Egorikreqwrqwerqwr1233224',
#     'interests': 'Egor21',
#     'z': 'абракадабра',
#     'height': 'dada',
#     'education': 'fdsfsdfs'
# })
#
# print(res.json())

# res = requests.get('http://127.0.0.1:5000/user_info/Egorik2242')
# print(res.json())

from s3 import s3
# # photo = "D:\wall\e8738644ceea3c8a3d29a798e71004d9.jpg"
# photo = 'w1.jpg'
# with open(photo, 'wb') as data:
#     s3.download_file(data, 'Egorik_e8738644ceea3c8a3d29a798e71004d9.jpg')
# s3.download_file('w2.jpg', 'Egorik_e8738644ceea3c8a3d29a798e71004d9.jpg')


# import requests
#
# res = requests.post('http://127.0.0.1:5000/login', json={
#     'login': 'Egorik22',
#     'password': 'qwert2y'
# })
#
# print(res.json())

#
res = requests.post('http://127.0.0.1:5000/down_photos/Egorik')
print(res.text)


