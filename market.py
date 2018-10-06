
from matplotlib import pyplot as plt
import numpy as np
import pulp
from itertools import product

from transactions import Transaction, Transactions
from actors import ActorsGroup


class Market:

    def __init__(self, actors_group: ActorsGroup):
        """
        Market constructor
        :param generation_bids:
        :param demand_bids:
        """

        generation_bids = actors_group.get_generator_bids()

        demand_bids = actors_group.get_consumer_bids()

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

        # declare alpha
        for i, j in product(range(ni), range(nj)):
            alpha[i, j] = pulp.LpVariable('alpha_' + str(i) + '_' + str(j), 0, 1)

        gen_slack = np.empty(nj, dtype=object)
        for j in range(nj):
            gen_slack[j] = pulp.LpVariable('gen_slack_' + str(j))

        # objective function
        f = 0
        for i, j in product(range(ni), range(nj)):
            f += self.demand_bids[i].energy_mw * alpha[i, j] * self.generation_bids[j].price
        prob += f #+ sum(gen_slack)

        #
        for j in range(nj):
            d_alpha = 0
            for i in range(ni):
                d_alpha += self.demand_bids[i].energy_mw * alpha[i, j]
            prob += (d_alpha <= self.generation_bids[j].energy_mw )#+ gen_slack[j])

        # sum of alpha per demand contract must be one
        for i in range(ni):
            prob += (sum(alpha[i, :]) == 1.0)

        # solve
        prob.solve()
        prob.writeLP('problem.lp')
        prob.writeMPS('problem.mps')
        print("Status:", pulp.LpStatus[prob.status], prob.status)

        #  -------------------------------------------------------------------------------------------------------------
        #  Generate the transactions

        transactions = Transactions()

        # problem solved
        for i, j in product(range(ni), range(nj)):
            id_gen = self.generation_bids[j].id
            id_demnd = self.demand_bids[i].id
            demand = self.demand_bids[i].energy_mw
            price = self.generation_bids[j].price
            val = alpha[i, j].value()
            if val != 0:
                print(id_demnd, 'buys from', id_gen, 'alpha', val)
                tr = Transaction(bid_id=str(id_gen) + '_' + str(id_demnd),
                                 seller_id=id_gen,
                                 buyer_id=id_demnd,
                                 energy_amount=val * demand,
                                 price=price,
                                 bid_type=self.demand_bids[i].bid_type)
                transactions.append(tr)

        return sorted(transactions, key=lambda x: x.bid_type, reverse=False)


    def plot(self):

        fig = plt.figure()
        ax = fig.add_subplot(111)

        ax.plot(self.generation_aggregated_price, label='Generation bids')
        ax.plot(self.demand_bids[0] - self.demand_aggregated_price, label='Demand bids')





