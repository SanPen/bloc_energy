from GridCal.Engine.All import *
from transactions import Transaction, Transactions
import numpy as np


def transaction_checking(grid: MultiCircuit, transactions: Transactions, agent_id_to_grid_id):
    """

    :param grid:
    :param transactions:
    :param agent_id_to_grid_id:
    :return:
    """

    load_ids = grid.get_load_names()
    loads = grid.get_loads()

    gen_ids = np.r_[grid.get_controlled_generator_names(), grid.get_battery_names()]




    load_dict = {}

    for transaction in transactions:

        # add power
        gen_id = agent_id_to_grid_id[transaction.seller_id]
        load_id = agent_id_to_grid_id[transaction.buyer_id]

