import requests
import json

url = 'http://localhost:5000/chain'

response = requests.get(url=url)

chain = json.loads(response._content)['chain']

print(response)
print(json.dumps(chain, indent=True))