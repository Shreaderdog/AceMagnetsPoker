from enums import Rank, Suit


class Card:
    rank = None
    suit = None

    def __init__(self, r, s):
        self.rank = r
        self.suit = s

    def getsuit(self):
        return self.suit.value

    def getrank(self):
        return self.rank.value

    def getplainsuit(self):
        return self.suit.name

    def getplainrank(self):
        return self.rank.name
