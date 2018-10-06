from enum import Enum
from matplotlib import pyplot as plt
import numpy as np
import pulp
from itertools import product


class BidType (Enum):
    obligatoria = 1,
    gestionable = 2,
    prescindible = 3


class Bid:
    def __init__(self, bid_type: BidType, energy_mw_, price_):
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
        return [Bid(BidType.obligatoria, self.energy_mw, self.price) ]


class Market:

    def __init__(self, generation_bids, demand_bids):
        """
        Market constructor
        :param generation_bids:
        :param demand_bids:
        """

        # sort by price
        self.generation_bids = sorted(generation_bids, key=lambda x: x.price, reverse=False)

        # sort by price
        self.demand_bids = sorted(demand_bids, key=lambda x: x.price, reverse=False)

        self.generation_aggregated_price = np.cumsum([elm.price for elm in self.generation_bids])

        self.demand_aggregated_price = np.cumsum([elm.price for elm in self.generation_bids])

    # def bid_matching(self):
    #
    #     for p in sorted(self.generation_aggregated_price + self.demand_aggregated_price):
    #         cum_dem = [ (p.x, p.y) for p in generation_aggregated_price if p.x < p ]

    def bid_matching(self):

        prob = pulp.LpProblem("DC optimal power flow", pulp.LpMinimize)

        ni = len(self.demand_bids)
        nj = len(self.generation_bids)

        alpha = np.empty((ni, nj), dtype=object)

        # objective function
        f = 0
        for i, j in product(range(ni), range(nj)):
            alpha[i, j] = pulp.LpVariable('alpha_' + str(i) + '_' + str(j), 0, 1)

            f += self.demand_bids[i].energy_mw * alpha[i, j] * self.generation_bids[j].price

        prob += f
        for j in range(nj):
            d_alpha = 0
            for i in range(ni):
                d_alpha += self.demand_bids[i].energy_mw * alpha[i, j]
            prob += pulp.LpConstraint(d_alpha <= self.generation_bids[j].price)



        for j in range(nj):
            d_alpha = 0
            for i in range(ni):
                d_alpha += alpha[i, j]
            prob += pulp.LpConstraint(d_alpha == 1.0)



        prob.solve()
        prob.writeLP('problem.lp')
        print("Status:", pulp.LpStatus[prob.status], prob.status)


        # problem solved
        for i, j in product(range(ni), range(nj)):
            val = alpha[i, j].value()
            if val > 0:
                print('demand ', i, 'generation ', j, 'alpha', val)

    def plot(self):

        fig = plt.figure()
        ax = fig.add_subplot(111)

        ax.plot(self.generation_aggregated_price, label='Generation bids')
        ax.plot(self.demand_bids[0] - self.demand_aggregated_price, label='Demand bids')


if __name__ == '__main__':

    consumidor_1 = Consumer(1, [Bid(BidType.obligatoria, 10, 200),
                                Bid(BidType.gestionable, 30, 25),
                                Bid(BidType.prescindible, 50, 5)])

    consumidor_2 = Consumer(2, [Bid(BidType.obligatoria, 50, 200),
                                Bid(BidType.gestionable, 30, 25),
                                Bid(BidType.prescindible, 50, 5)])

    generator_1 = Generator(1, energy_mw_=10, price_=100)
    generator_2 = Generator(2, energy_mw_=20, price_=20)
    generator_3 = Generator(3, energy_mw_=100000000, price_=100)

    consumer_list = [ consumidor_1, consumidor_2 ]
    generator_list = [ generator_1, generator_2, generator_3 ]

    consumer_bids = []
    for consumer in consumer_list:
        consumer_bids += consumer.generate_bids()

    generator_bids = []
    for generator in generator_list:
        generator_bids += generator.generate_bids()

    market = Market(generation_bids=generator_bids, demand_bids=consumer_bids)

    market.bid_matching()


