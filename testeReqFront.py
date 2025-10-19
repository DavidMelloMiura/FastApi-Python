import requests

headers = {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI4IiwiZXhwIjoxNzYwODExOTgyfQ.2jRQGF6LEfqjFSOv1kMQ6G7Tq3lSnLzXNTCgd2ESKPw"
}

req = requests.get("http://127.0.0.1:8000/auth/refresh", headers=headers)
print(req)
print(req.json())
