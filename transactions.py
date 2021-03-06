from collections import MutableSequence
from bidding import BidType
import json

class Transaction:

    def __init__(self, bid_id, seller_id, buyer_id, energy_amount, price, bid_type: BidType, bid_hash=None):
        """
        Power Transaction
        :param bid_id:
        :param seller_id:
        :param buyer_id:
        :param energy_amount: amount of energy (in MWh)
        :param price: amount of price (€ / MWh)
        :param bid_type:
        :param bid_hash: computed hash function
        """
        self.bid_id = bid_id

        self.seller_id = seller_id

        self.buyer_id = buyer_id

        self.energy_amount = energy_amount

        self.price = price

        if type(bid_type) is BidType:
            try:
                self.bid_type = bid_type.value[0]
            except:
                self.bid_type = bid_type.value
        else:
            self.bid_type = int(bid_type)

        self.hash = bid_hash

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)

    def __str__(self):
        return self.to_json()

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

    def __str__(self):

        val = ''

        for elm in self.transactions:
            val += elm.to_json()

        return val
