from enum import Enum

class Tipo (Enum):
    obligatoria = 1
    gestionable = 2
    prescindible = 3

class Bid:
    def __init__(self, tipo_, energy_mw_, prize_):
        self.tipo = tipo_
        self.energy_mw = energy_mw_
        self.prize = prize_

class Consumer:
    def generate_bids(list_bids_):
        return list_bids_
    def __init__(self, consumer_bids_, id_):
        self.consumer_bids = consumer_bids
        self.id = id_

class Generator:
    def __init__(self, energy_mw_, prize_):
        self.id = id_
        self.energy_mw = energy_mw_
        self.prize = prize_

class Casacion:
    def main():
        self.consumidor_1 = Consumer( [ Bid(1, 10, 200), Bid(2, 30, 25), Bid(3, 50, 5) ] )
        self.consumidor_2 = Consumer( [ Bid(1, 50, 200), Bid(2, 30, 25), Bid(3, 50, 5) ] )
        self.generator_1 = Generator( 10, 100 )
        self.generator_2 = Generator(20, 20)
        self.generator_3 = Generator(30, inf)
        consumers =  [ consumidor_1, consumidor_2 ]
        generators = [ generator_1, generator_2, generator_3]

