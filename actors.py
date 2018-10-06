
from bidding import Bid


class Consumer:

    def __init__(self, id_):
        self.id = id_
        self.bids = list()

    def generate_bids(self):
        return [Bid(self.id, bid) for bid in self.bids]


class Generator:

    def __init__(self, id_):
        self.id = id_
        self.bids = list()

    def generate_bids(self):
        return [Bid(self.id, bid) for bid in self.bids]


class ActorsGroup:

    def __init__(self):
        """

        """
        self.consumer_list = list()
        self.generator_list = list()

    def add_generator(self, elm):
        """

        :param elm:
        :return:
        """
        self.generator_list.append(elm)

    def add_consumer(self, elm):
        """

        :param elm:
        :return:
        """
        self.consumer_list.append(elm)

    def get_consumer_bids(self):
        """

        :return:
        """
        consumer_bids = list()
        for consumer in self.consumer_list:
            consumer_bids += consumer.generate_bids()

        return consumer_bids

    def get_generator_bids(self):
        """

        :return:
        """
        generator_bids = list()
        for generator in self.generator_list:
            generator_bids += generator.generate_bids()

        return generator_bids

