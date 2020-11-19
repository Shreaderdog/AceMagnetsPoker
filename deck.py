import card, random
from enums import Rank, Suit


class Deck:
    cards = []

    def __init__(self):
        for suit in Suit:
            for rank in Rank:
                self.cards.append(card.Card(rank, suit))

    def deal(self, n, h):
        for i in range(0, n):
            h.add_card(self.cards[0])
            del self.cards[0]

    def shuffle(self):
        random.shuffle(self.cards)
