import unittest, deck, hand, card, player, main
from enums import Rank, Suit

class functionTest(unittest.TestCase):

# deck tests
    def test_deck_length(self):
        td = deck.Deck()
        self.assertTrue(len(td.cards) == 52) # checks for 52 cards

    def test_deck_unique(self):
        td = deck.Deck()
        self.assertTrue(len(td.cards) == len(set(td.cards)))  # checks all unique

    def test_deck_shuffle(self):
        td = deck.Deck()
        h1 = hand.Hand()
        td.deal(5, h1)
        td = deck.Deck()
        h2 = hand.Hand()
        td.shuffle()
        td.deal(5, h2)
        self.assertTrue(h1.get_cards() == h2.get_cards())

# flushcheck tests

    def test_flush_check(self):
        clist = []
        clist.append(card.Card(Rank.two, Suit.c))
        clist.append(card.Card(Rank.three, Suit.c))
        clist.append(card.Card(Rank.four, Suit.c))
        clist.append(card.Card(Rank.six, Suit.c))
        clist.append(card.Card(Rank.eight, Suit.c))
        self.assertTrue(main.flush(clist))

    def test_straight_check(self):
        clist = []
        clist.append(card.Card(Rank.two, Suit.c))
        clist.append(card.Card(Rank.three, Suit.c))
        clist.append(card.Card(Rank.four, Suit.c))
        clist.append(card.Card(Rank.five, Suit.c))
        clist.append(card.Card(Rank.six, Suit.d))
        self.assertTrue(main.straight(clist))


if __name__ == '__main__':
    unittest.main()
