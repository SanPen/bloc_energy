import requests


url = 'http://localhost:5000/chain'

response = requests.get(url=url)

print(response)