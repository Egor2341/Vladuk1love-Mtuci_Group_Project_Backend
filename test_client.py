# from app import client
from requests import post, get
from pprint import pprint
# res = client.get('/smth')
# client.post('smth', json={})
# res = client.
# res = client.get("/session_test")
# for i in range(1, 30):
res = get('http://127.0.0.1:5000/found_users_on_the_main_page/dawud2', json={'sex': ['Male', 'Female'],
                                                                             'age': 'any',
                                                                             'purpose': 'any'})
js = res.json()
pprint(js)
# for i in js.items():
#     pprint(i)
# for i in range(1, 30):
#     res = post('http://127.0.0.1:5000/registration', json={'name': f'david{i}',
#                                                            'login': f"dawud{i}",
#                                                            'age': i + 10,
#                                                            'sex': "Male",
#                                                            'password': f'pedikules{i}'
#                                                            })
#     print(res.json)
json = {'filters': {'sex': 53,
                    'age': 'any',
                    'dating_purpose': 'any'}}
