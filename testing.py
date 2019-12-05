import unittest
from classes import Token, Deck

class TestToken(unittest.TestCase):

    def test_intended_use(self):
        # test standard instantiation
        token = Token("gold", 6)
        self.assertEqual(token.name, "gold")
        self.assertEqual(token.value, 6)

    def test_for_illegal_names(self):
        # test for goods that don't exist
        with self.assertRaises(ValueError):
            Token("pineapple", 1)

    def test_for_illegal_values(self):
        # test for zero or negative values
        with self.assertRaises(ValueError):
            Token("leather", -3)
        # test for non integer values
        with self.assertRaises(ValueError):
            Token("cloth", 4.7)
        with self.assertRaises(ValueError):
            Token("spice", 2.0)

class TestDeck(unittest.TestCase):

    def setUp(self):
        self.deck = Deck(default=True)
        self.initial_deck_len = len(self.deck)

    def tearDown(self):
        del self.deck
        del self.initial_deck_len

    def test_draw_default(self):
        drawn_cards = self.deck.draw()
        self.assertEqual(len(drawn_cards), 1)
        self.assertEqual(len(self.deck), self.initial_deck_len-1)

    def test_draw_multiple(self):
        drawn_cards = self.deck.draw(3)
        self.assertEqual(len(drawn_cards), 3)
        self.assertEqual(len(self.deck), self.initial_deck_len-3)

    def test_draw_too_many(self):
        # draw exactly the number of cards left in the deck
        self.deck = Deck(camel=5)
        drawn_cards = self.deck.draw(5)
        self.assertEqual(drawn_cards, ["camel"]*5)
        self.assertEqual(len(self.deck), 0)

        # drawing too many cards should just return available cards
        self.deck = Deck(camel=5)
        drawn_cards = self.deck.draw(10)
        self.assertEqual(drawn_cards, ["camel"]*5)
        self.assertEqual(len(self.deck), 0)

        # draw from an empty deck should return empty list
        self.deck = Deck()
        drawn_cards = self.deck.draw()
        self.assertEqual(drawn_cards, [])
        self.assertEqual(len(self.deck), 0)

        self.deck = Deck()
        drawn_cards = self.deck.draw(10)
        self.assertEqual(drawn_cards, [])
        self.assertEqual(len(self.deck), 0)

    def test_take(self):
        drawn_cards = self.deck.take("camel")
        self.assertEqual(len(drawn_cards), 1)
        self.assertEqual(drawn_cards, ["camel"])

    def test_take_too_many(self):
        with self.assertRaises(ValueError):
            self.deck.take("camel", 100)

    def test_take_when_card_not_present(self):
        # try to draw a card that isn't in the deck
        with self.assertRaises(ValueError):
             self.deck.take("magic carpet")

    def test_take_multiple(self):
        drawn_cards = self.deck.take("silver", 5)
        # check correct number and type of drawn cards
        self.assertEqual(len(drawn_cards), 5)
        self.assertEqual(drawn_cards, ["silver"]*5)
        # check deck reduced in size correctly
        self.assertEqual(len(self.deck), self.initial_deck_len-5)

    def test_shuffle(self):
        unshuffled_deck = self.deck.copy()
        self.deck.shuffle()
        shuffled_deck = self.deck.copy()
        self.assertNotEqual(unshuffled_deck, shuffled_deck)

    def test_peek(self):
        # check correct number of cards seen
        seen_cards = self.deck.peek()
        self.assertEqual(len(seen_cards), 1)
        seen_cards = self.deck.peek(4)
        self.assertEqual(len(seen_cards), 4)

        # check that the peeking didn't change the number of cards in the deck
        self.assertEqual(len(self.deck), self.initial_deck_len)

if __name__ == "__main__":
    unittest.main()