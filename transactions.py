from collections import MutableSequence
from GridCal.Engine.All import *


class Transaction:

    def __init__(self, bid_id, seller_id, buyer_id, energy_amount, price, tipology, hash):

        self.bid_id = bid_id

        self.seller_id = seller_id

        self.buyer_id = buyer_id

        self.energy_amount = energy_amount

        self.price = price

        self.tipology = tipology

        self.hash = hash


class Transactions(MutableSequence):
    """
    Class to store he transactions
    """

    def __init__(self, lst=list()):

        if type(lst) is not list:
            raise ValueError()

        self.transactions = lst

    def __len__(self):
        return len(self.transactions)

    def __delitem__(self, index):
        self.transactions.__delitem__(index - 1)

    def insert(self, index, value):
        self.transactions.insert(index - 1, value)

    def __setitem__(self, index, value):
        self.transactions.__setitem__(index - 1, value)

    def __getitem__(self, index):
        return self.transactions.__getitem__(index - 1)


def check_transaction(grid: MultiCircuit, V0, S0, transaction: Transaction):

    pass