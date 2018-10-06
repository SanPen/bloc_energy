from collections import MutableSequence
# from GridCal.Engine.All import *
from bidding import BidType


class Transaction:

    def __init__(self, bid_id, seller_id, buyer_id, energy_amount, price, bid_type: BidType, hash=None):
        """
        Power Transaction
        :param bid_id:
        :param seller_id:
        :param buyer_id:
        :param energy_amount: amount of energy (in MWh)
        :param price: amount of price (€ / MWh)
        :param bid_type:
        :param hash: computed hash function
        """
        self.bid_id = bid_id

        self.seller_id = seller_id

        self.buyer_id = buyer_id

        self.energy_amount = energy_amount

        self.price = price

        # TODO: Review this WTF
        try:
            self.bid_type = bid_type.value[0]
        except:
            self.bid_type = bid_type.value

        self.hash = hash

    def __le__(self, other):
        return self.bid_type < other.bid_type


class Transactions(MutableSequence):
    """
    Class to store the transactions
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


# def check_transaction(grid: MultiCircuit, transaction: Transaction):
#
#     options = PowerFlowOptions()
#
#     pf = PowerFlow(grid, options)
#
#     pf.run()
#
#     results = pf.results
