from GridCal.Engine.All import *
from transactions import Transaction, Transactions
import numpy as np
import hashlib


def transaction_mine(grid: MultiCircuit, transaction: Transaction, agent_id_to_grid_id, dt=1):
    """
    Mine a transaction with the technical calculation
    :param grid: GridCal grid Object
    :param transaction: Transaction object
    :param agent_id_to_grid_id: dictionary to relate the agent's id with the grid object's id
    :param dt: market interval in hours
    :return: hash (if the hash is none, the solution is not valid)
    """

    # declare the power flow options
    options = PowerFlowOptions()

    load_ids = grid.get_load_names()
    loads = grid.get_loads()
    gen_ids = np.r_[grid.get_controlled_generator_names(), grid.get_battery_names()]
    gens = np.r_[grid.get_controlled_generators(), grid.get_batteries()]
    load_dict = {load_ids[i]: loads[i] for i in range(len(loads))}
    gen_dict = {gen_ids[i]: gens[i] for i in range(len(gens))}

    # get the objects
    gen_id = agent_id_to_grid_id[transaction.seller_id]
    load_id = agent_id_to_grid_id[transaction.buyer_id]
    load = load_dict[load_id]
    gen = gen_dict[gen_id]

    # add power
    load.S = -complex(transaction.energy_amount / dt, load.S.imag)
    gen.P = transaction.energy_amount / dt

    # run the calculation
    pf = PowerFlow(grid, options)
    pf.run()

    # Compute the error number
    v = np.abs(pf.results.voltage)
    nerr = len(np.where(v > 1.1)[0])
    nerr += len(np.where(v < 0.9)[0])
    nerr += len(np.where(pf.results.loading > 1)[0])

    if nerr == 0:
        hash = hashlib.sha3_256(pf.results.voltage).hexdigest()
    else:
        hash = None

    return hash


def transaction_checking(grid: MultiCircuit, transactions: Transactions, agent_id_to_grid_id, dt=1):
    """
    Function that checks the transactions with electrical computations
    :param grid: GridCal grid Object
    :param transactions: Transactions object
    :param agent_id_to_grid_id: dictionary to relate the agent's id with the grid object's id
    :param dt: market interval in hours
    :return:
    """

    # declare the final transactions list
    final_transactions = Transactions()

    for transaction in transactions:

        hash = transaction_mine(grid, transaction, agent_id_to_grid_id, dt=dt)

        # if there are no errors
        if hash is not None:
            # modify the transaction, adding a hash based on the voltage
            transaction.hash = hash

            # store the transaction
            final_transactions.append(transaction)
        else:
            # since the transactions are sorted, if a critical state is found the rest are curtailed
            return final_transactions

    # return the approved transactions
    return final_transactions

