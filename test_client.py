from app import client
from requests import post
# res = client.get('/smth')
# client.post('smth', json={})
res = client.post('/login', json={'email': 'bbbb@gmail.com', 'password': "12345"})
# res = client.get("/session_test")
# res = post('http://127.0.0.1:5000/registration', json={'name': 'MY_NEW_USER', 'email': 'WINNER@gmail.com', 'password': "525252"})
print(res.get_json())

