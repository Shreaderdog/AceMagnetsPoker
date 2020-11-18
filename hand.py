import card


class Hand:
    cards = []
    swaps = []

    def __init__(self):
        cards = []

    def add_card(self, s):
        self.cards.append(s)

    def remove_card(self, s):
        del self.cards[s]

    def get_cards(self):
        return self.cards

    def addswaps(self, num):
        self.swaps.append(num)

    def removeswaps(self, num):
        self.swaps.remove(num)

    def getswaps(self):
        return self.swaps

    def clear(self):
        self.cards = []
        self.swaps = []
