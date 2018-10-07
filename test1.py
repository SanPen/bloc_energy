from actors import Consumer, Generator, ActorsGroup
from market import Market
from bidding import BidType, ActorBid
from grid import MultiCircuit, transaction_checking
from ConsumerFactory import ConsumerFactory, GeneratorFactory

if __name__ == '__main__':

    consumer_1 = Consumer('Consumer1')
    consumer1bids = ConsumerFactory(1,fpath = 'consumer1.csv', maximum_price=200).getbid(1)
    consumer_1.bids = [ActorBid(BidType.Compulsory, consumer1bids[0][0][1], consumer1bids[0][0][2]),
                       ActorBid(BidType.Manageable,  consumer1bids[1][0][1], consumer1bids[1][0][2]),
                       ActorBid(BidType.Expendable,  consumer1bids[2][0][1], consumer1bids[2][0][2])]

    consumer_2 = Consumer('Consumer2')
    consumer2bids = ConsumerFactory(1, fpath='consumer2.csv', maximum_price=195).getbid(1)
    consumer_2.bids = [ActorBid(BidType.Compulsory, consumer2bids[0][0][1], consumer2bids[0][0][2]),
                       ActorBid(BidType.Manageable,  consumer2bids[1][0][1], consumer2bids[1][0][2]),
                       ActorBid(BidType.Expendable,  consumer2bids[2][0][1], consumer2bids[2][0][2])]

    generator_1 = Generator('Gen1')
    gen1bid = GeneratorFactory('solargen.csv', scale_factor=50, max_price=100).getbid()
    generator_1.bids = [ActorBid(BidType.Compulsory, gen1bid[1],gen1bid[2])]

    generator_2 = Generator('Gen2')
    #generator_2.bids = [ActorBid(BidType.Compulsory, energy_mw_=20, price_=20)]
    gen2bid = GeneratorFactory('solargen.csv', scale_factor=10, max_price=20).getbid()
    generator_2.bids = [ActorBid(BidType.Compulsory, gen2bid[1], gen2bid[2])]

    generator_3 = Generator('Gen3')
    #generator_3.bids = [ActorBid(BidType.Compulsory, energy_mw_=10000, price_=100)]
    gen1bid = GeneratorFactory('solargen.csv', scale_factor=300, max_price=103).getbid()
    generator_1.bids = [ActorBid(BidType.Compulsory, gen1bid[1], gen1bid[2])]

    group = ActorsGroup()
    group.add_consumer(consumer_1)
    group.add_consumer(consumer_2)

    group.add_generator(generator_1)
    group.add_generator(generator_2)
    group.add_generator(generator_3)

    market = Market(actors_group=group)

    transactions = market.bid_matching()

    # load grid
    grid = MultiCircuit()
    grid.load_file('Grid.xlsx')

    agent_id_to_grid_id = {'Consumer1': '',
                           'Consumer2': '',
                           'Gen1': '',
                           'Gen2': '',
                           'Gen3': ''}

    transaction_checking(grid=grid, transactions=transactions, agent_id_to_grid_id=agent_id_to_grid_id)
