import hand

class Player:
    name = ""
    currency = 0
    phand = hand.Hand()

    def __init__(self, n, a):
        self.name = n
        self.currency = a

    def add_currency(self, a):
        self.currency += a

    def remove_currency(self, a):
        self.currency -= a
