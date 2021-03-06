
from enum import Enum


class BidType (Enum):
    Compulsory = 1,
    Manageable = 2,
    Expendable = 3


class ActorBid:

    def __init__(self, bid_type: BidType, energy_mw_, price_):
        """

        :param bid_type:
        :param energy_mw_:
        :param price_:
        """
        self.bid_type = bid_type
        self.energy_mw = energy_mw_
        self.price = price_


class Bid:

    def __init__(self, actor_id, bid):
        """

        :param bid_type:
        :param energy_mw_:
        :param price_:
        """
        self.id = actor_id
        self.bid_type = bid[0]
        self.energy_mw = bid[1]
        self.price = bid[2]

    def __str__(self):
        return str(self.id) + ' e:' + str(self.energy_mw) + ' pr:' + str(self.price)