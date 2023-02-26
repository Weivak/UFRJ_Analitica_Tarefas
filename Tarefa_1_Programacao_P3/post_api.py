import requests

url = 'http://127.0.0.1:5000'

data = {
    'name': 'Thalita de Melo',
    'birthdate': '1995-09-10',
    'date': '2024-11-09'
}

response = requests.post(url, json=data)

print(response.json())