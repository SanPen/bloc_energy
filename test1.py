from actors import Consumer, Generator, ActorsGroup
from market import Market
from bidding import BidType, ActorBid


if __name__ == '__main__':

    consumer_1 = Consumer('Consumer1')
    consumer_1.bids = [ActorBid(BidType.Compulsory, 10, 200),
                       ActorBid(BidType.Manageable, 30, 25),
                       ActorBid(BidType.Expendable, 50, 5)]

    consumer_2 = Consumer('Consumer2')
    consumer_2.bids = [ActorBid(BidType.Compulsory, 50, 200),
                       ActorBid(BidType.Manageable, 30, 25),
                       ActorBid(BidType.Expendable, 50, 5)]

    generator_1 = Generator('Gen1')
    generator_1.bids = [ActorBid(BidType.Compulsory, energy_mw_=10, price_=100)]

    generator_2 = Generator('Gen2')
    generator_2.bids = [ActorBid(BidType.Compulsory, energy_mw_=20, price_=20)]

    generator_3 = Generator('Gen3')
    generator_3.bids = [ActorBid(BidType.Compulsory, energy_mw_=10000, price_=100)]

    group = ActorsGroup()
    group.add_consumer(consumer_1)
    group.add_consumer(consumer_2)

    group.add_generator(generator_1)
    group.add_generator(generator_2)
    group.add_generator(generator_3)

    market = Market(actors_group=group)

    transactions = market.bid_matching()
