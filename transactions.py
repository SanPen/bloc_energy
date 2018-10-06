

class Transaction:

    def __init__(self, bid_id, seller_id, buyer_id, energy_amount, price, tipology, hash):

        self.bid_id = bid_id

        self.seller_id = seller_id

        self.buyer_id = buyer_id

        self.energy_amount = energy_amount

        self.price = price

        self.tipology = tipology

        self.hash = hash