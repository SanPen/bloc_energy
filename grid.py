from GridCal.Engine.All import *
from transactions import Transaction, Transactions
import numpy as np
import hashlib


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
    gens = np.r_[grid.get_controlled_generators(), grid.get_batteries()]

    load_dict = {load_ids[i]: loads[i] for i in range(len(loads))}
    gen_dict = {gen_ids[i]: gens[i] for i in range(len(gens))}

    options = PowerFlowOptions()

    results = list()

    numerical_circuit = grid.compile()
    calculation_inputs = numerical_circuit.compute()

    final_transactions = Transactions()

    for transaction in transactions:

        # get the objects
        gen_id = agent_id_to_grid_id[transaction.seller_id]
        load_id = agent_id_to_grid_id[transaction.buyer_id]
        load = load_dict[load_id]
        gen = gen_dict[gen_id]

        # add power
        load.S = -complex(transaction.energy_amount, load.S.imag)
        gen.P = transaction.energy_amount

        # run the calculation
        pf = PowerFlow(grid, options)
        pf.run()

        # gather results
        results.append([pf.results.voltage, pf.results.loading])

        errors = pf.results.check_limits(F=calculation_inputs.F, T=calculation_inputs.T,
                                         Vmax=calculation_inputs.Vmax, Vmin=calculation_inputs.Vmin)

        if errors == 0:
            transaction.hash = hashlib.sha3_256(errors).hexdigest()
            final_transactions.append(transaction)

    return final_transactions

