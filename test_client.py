# from app import client
from requests import post, get, put
from pprint import pprint

# res = client.get('/smth')
# client.post('smth', json={})
# res = client.
# res = client.get("/session_test")
# for i in range(1, 30):
res = post('http://127.0.0.1:5000/likes/egor',
           json={'who_i_liked': 'sergey'
                 }
           )
js = res.json()
pprint(js)

res = get('http://127.0.0.1:5000/who_liked_me/vlad')
js = res.json()
pprint(js)
# for i in js.items():
#     pprint(i)
# for i in range(30):
#     res = post('http://127.0.0.1:5000/registration', json={'name': f'david{i}',
#                                                            'login': f"dawud{i}",
#                                                            'age': i + 10,
#                                                            'sex': "Female",
#                                                            'password': f'pedikules{i}'
#                                                            })
#     print(res.json)
# json = {'filters': {'sex': ['Male', 'Female', "Male or Female"],
#                     'age': [17, 24],
#                     'purpose': ['friendship', 'relationships', 'friendship or relationships']}}
# for i in range(30, 60):
#     res = put(f'http://127.0.0.1:5000/user_info/dawud{i}',
#               json={'about_me': 'about_me',
#                     'interests': 'interests',
#                     'group': 'group',
#                     'dating_purpose': 'friendship',
#                     'education': 'education'}
#               )
#     print(res.json())
