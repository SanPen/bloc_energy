import requests


# r = requests.get('https://api.spotify.com/v1/search?type=artist&q=snoop')
# r.json()

import requests
import urllib.request
import json
from actors import Consumer, Generator, ActorsGroup
from market import Market
from bidding import BidType, ActorBid
from grid import MultiCircuit, transaction_checking
from ConsumerFactory import ConsumerFactory, GeneratorFactory


consumer_1 = Consumer('Consumer1')
consumer1bids = ConsumerFactory(1, fpath='consumer1.csv', maximum_price=200).getbid(1)
bids = [[1, consumer1bids[0][0][1], consumer1bids[0][0][2]],
        [2,  consumer1bids[1][0][1], consumer1bids[1][0][2]],
        [3,  consumer1bids[2][0][1], consumer1bids[2][0][2]]]

header = {'id': 'Consumer1',
         'grid_id': 'Load@Bloque de pisos',
         'bids': bids}


requests.post('http://127.0.0.1:5000/transactions/addconsumer', json=json.dumps(header))

# res = urllib.request.urlopen(req, timeout=5)
#
# print(res.status)
# print(res.reason)
