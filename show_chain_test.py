import requests


url = 'http://localhost:5000/nodes/resolve'

response = requests.get(url=url)

print(response)