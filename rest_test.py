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
agent_id_to_grid_id = {'Consumer1': 'Load@Bloque de pisos',
                           'Consumer2': 'Load@Bus 3',
                           'Consumer3': 'Load@fabrica',
                           'Consumer4': 'Load@Bus 5',
                           'Consumer5': 'Load@Bus 7',
                           'Consumer6': 'Load@compañia',
                           'Gen1': 'gen_huerto_solar',
                           'Gen2': 'gen_bus_5',
                           'Gen3': 'gen_bloque_pisos'}

consumer_1 = Consumer('Consumer1')
consumer1bids = ConsumerFactory(1, fpath='consumer1.csv', maximum_price=200).getbid(1)
bids = [[1, consumer1bids[0][0][1], consumer1bids[0][0][2]],
        [2,  consumer1bids[1][0][1], consumer1bids[1][0][2]],
        [3,  consumer1bids[2][0][1], consumer1bids[2][0][2]]]

header = {'id': 'Consumer1',
         'grid_id': agent_id_to_grid_id['Consumer1'],
         'bids': bids}
requests.post('http://127.0.0.1:5000/transactions/addconsumer', json=json.dumps(header))


consumer_2 = Consumer('Consumer2')
consumer2bids = ConsumerFactory(1, fpath='consumer2.csv', maximum_price=200).getbid(1)
bids2 = [[1, consumer2bids[0][0][1], consumer2bids[0][0][2]],
        [2,  consumer2bids[1][0][1], consumer2bids[1][0][2]],
        [3,  consumer2bids[2][0][1], consumer2bids[2][0][2]]]

header2 = {'id': 'Consumer2',
         'grid_id':  agent_id_to_grid_id['Consumer2'],
         'bids': bids2}
requests.post('http://127.0.0.1:5000/transactions/addconsumer', json=json.dumps(header2))

consumer_3 = Consumer('Consumer3')
consumer3bids = ConsumerFactory(1, fpath='consumer3.csv', maximum_price=200).getbid(1)
bids3 = [[1, consumer2bids[0][0][2], consumer2bids[0][0][2]],
        [2,  consumer2bids[2][0][2], consumer2bids[2][0][2]],
        [3,  consumer2bids[2][0][2], consumer2bids[2][0][2]]]

header3 = {'id': 'Consumer3',
         'grid_id':  agent_id_to_grid_id['Consumer3'],
         'bids': bids3}
requests.post('http://127.0.0.1:5000/transactions/addconsumer', json=json.dumps(header3))

consumer_4 = Consumer('Consumer4')
consumer4bids = ConsumerFactory(1, fpath='consumer1.csv', maximum_price=200).getbid(1)
bids4 = [[1, consumer2bids[0][0][2], consumer2bids[0][0][2]],
        [2,  consumer2bids[2][0][2], consumer2bids[2][0][2]],
        [3,  consumer2bids[2][0][2], consumer2bids[2][0][2]]]

header4 = {'id': 'Consumer4',
         'grid_id':  agent_id_to_grid_id['Consumer4'],
         'bids': bids4}
requests.post('http://127.0.0.1:5000/transactions/addconsumer', json=json.dumps(header4))

consumer_5 = Consumer('Consumer5')
consumer5bids = ConsumerFactory(1, fpath='consumer2.csv', maximum_price=200).getbid(1)
bids5 = [[1, consumer2bids[0][0][2], consumer2bids[0][0][2]],
        [2,  consumer2bids[2][0][2], consumer2bids[2][0][2]],
        [3,  consumer2bids[2][0][2], consumer2bids[2][0][2]]]

header5 = {'id': 'Consumer5',
         'grid_id':  agent_id_to_grid_id['Consumer5'],
         'bids': bids5}
requests.post('http://127.0.0.1:5000/transactions/addconsumer', json=json.dumps(header5))


consumer_6 = Consumer('Consumer6')
consumer5bids = ConsumerFactory(1, fpath='consumer3.csv', maximum_price=200).getbid(1)
bids6 = [[1, consumer2bids[0][0][2], consumer2bids[0][0][2]],
        [2,  consumer2bids[2][0][2], consumer2bids[2][0][2]],
        [3,  consumer2bids[2][0][2], consumer2bids[2][0][2]]]

header6 = {'id': 'Consumer6',
         'grid_id':  agent_id_to_grid_id['Consumer6'],
         'bids': bids6}
requests.post('http://127.0.0.1:5000/transactions/addconsumer', json=json.dumps(header6))



#['id', 'grid_id', 'bids']

generator_1 = Generator('Gen1')
gen1bid = GeneratorFactory('solargen.csv', scale_factor=50, max_price=100).getbid()
generator_1.bids = [[0, gen1bid[1], gen1bid[2]]]
headergen = {'id': 'Gen1',
             'grid_id':  agent_id_to_grid_id['Gen1'],
             'bids': generator_1.bids }
requests.post('http://127.0.0.1:5000/transactions/addgenerator', json=json.dumps(headergen))


generator_2 = Generator('Gen2')
# generator_2.bids = [ActorBid(BidType.Compulsory, energy_mw_=20, price_=20)]
gen2bid = GeneratorFactory('solargen.csv', scale_factor=5.5, max_price=95).getbid()
generator_2.bids = [[0, gen2bid[1], gen2bid[2]]]
headergen2 = {'id': 'Gen2',
            'grid_id':  agent_id_to_grid_id['Gen2'],
            'bids': generator_2.bids}
requests.post('http://127.0.0.1:5000/transactions/addgenerator', json=json.dumps(headergen2))

generator_3 = Generator('Gen3')
# generator_3.bids = [ActorBid(BidType.Compulsory, energy_mw_=10000, price_=100)]
gen3bid = GeneratorFactory('solargen.csv', scale_factor=300, max_price=103).getbid()
generator_1.bids = [[0, gen1bid[1], gen1bid[2]]]
headergen3 = {'id': 'Gen3',
            'grid_id':  agent_id_to_grid_id['Gen3'],
            'bids': generator_1.bids }
requests.post('http://127.0.0.1:5000/transactions/addgenerator', json=json.dumps(headergen3))

print('Exito posting consumer and generatos to blockchain')


# ----------------------------------------------------------------------------------------------------------------------
# Mine
url = 'http://localhost:5000/mine'

response = requests.get(url=url)

print(response)
# r--------------------------------------

url = 'http://localhost:5000/chain'

response = requests.get(url=url)

print(response)
