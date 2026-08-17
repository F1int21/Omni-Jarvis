import requests
response = requests.post('http://localhost:8000/command', json={'command': 'пропингуй 8.8.8.8'})
print(response.json())