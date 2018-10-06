from enum import Enum

class BidType (Enum):
    obligatoria = 1,
    gestionable = 2,
    prescindible = 3

class Bid:
    def __init__(self, bid_type: BidType, energy_mw_, prize_):
        self.tipo = bid_type
        self.energy_mw = energy_mw_
        self.price = price_

class Consumer:
    def generate_bids(self):
        return self.consumer_bids
    def __init__(self, id_, consumer_bids_):
        self.id = id_
        self.consumer_bids = consumer_bids_

class Generator:
    def __init__(self, id_, energy_mw_, price_):
        self.id = id_
        self.energy_mw = energy_mw_
        self.price = price_
    def generate_bids(self):
        return [ Bid(Tipo.obligatoria, self.energy_mw, self.price) ]

class Casacion:
    def __init__(self, generation_bids, demand_bids):
        self.generation_bids = generation_bids
        self.demand_bids = demand_bids

if __name__ == '__main__':

    consumidor_1 = Consumer([Bid(BidType.obligatoria, 10, 200),
                             Bid(BidType.gestionable, 30, 25),
                             Bid(BidType.prescindible, 50, 5)])

    consumidor_2 = Consumer([Bid(BidType.obligatoria, 50, 200),
                             Bid(BidType.gestionable, 30, 25),
                             Bid(BidType.prescindible, 50, 5)])

    generator_1 = Generator(10, 100)
    generator_2 = Generator(20, 20)
    generator_3 = Generator(30, 1e20)

    consumer_list = [ consumidor_1, consumidor_2 ]
    generator_list = [ generator_1, generator_2, generator_3 ]

    consumer_bids = []
    for consumer in consumer_list:
        consumer_bids += consumer.generate_bids()

    generator_bids = []
    for generator in generator_list:
        generator_bids += generator.generate_bids()


