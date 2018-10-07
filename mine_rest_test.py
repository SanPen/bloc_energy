import requests


url = 'http://localhost:5000/mine'

response = requests.get(url=url)

print(response)