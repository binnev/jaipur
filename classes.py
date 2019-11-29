from random import shuffle


class Token():
    """Represents the round goods tokens which give players points. Each token
    should have
    - a value (on the back)
    - the name (on the front) e.g. "diamond" or "triple combo"
    """

    def __init__(self, name, value):
        self.name = name
        self.value = value

    def __repr__(self):
        return f"{self.name} (worth {self.value})"


class Deck(list):
    def __init__(self, diamond=6, gold=6, silver=6, cloth=8, spice=8,
                 leather=10, camel=11):
        contents = (["diamond"] * diamond
                 + ["silver"] * silver
                 + ["gold"] * gold
                 + ["cloth"] * cloth
                 + ["spice"] * spice
                 + ["leather"] * leather
                 + ["camel"] * camel)
        super().__init__(contents)

    def shuffle(self):
        shuffle(self)

    def draw(self, number=1):
        return [self.pop() for __ in range(number)]

    def draw_specific(self, card, number=1):
        return [self.pop(self.index(card)) for __ in range(number)]

    def peek(self, depth=1):
        return self[-depth:]


class TokenStack(Deck):
    """Represents the stacks of tokens. Could be anything from the market goods
    to the Biggest Herd token to the combo tokens.
    Functionally very similar to the Deck class, but not limited to the card
    types
    """
    def __init__(self, *list_of_tokens):
        list.__init__(self, list(list_of_tokens))

    def sort_by_value(self, descending=True):
        """Sort the stack of tokens so that the highest value ones are on top.
        This means the highest value tokens should be the first to get popped
        off the list---meaning they should be at the end of the list.
        """
        self.sort(key=lambda x: x.value)

    def get_values(self):
        return [token.value for token in self]


class Marketplace(list):
    """Represents the 5 card river marketplace.
    Needs to keep track of empty spaces and/or preserve the order.
    """
    def __init__(self, list_of_5_cards):
        super().__init__(list_of_5_cards)

    def swap(self, player_card, market_card):
        """Swap one player card for one market card. Illegal move. Intended for
        use as part of the trade() method."""
        ind = self.index(market_card)
        out = self.pop(ind)            # remove card from market
        self.insert(ind, player_card)  # insert player card into same slot
        return out

class Game():
    def __init__(self):
        # create token piles
        # populate tokens dictionary
        self.tokens = {"diamond": [5, 5, 5, 7, 7],
                       "gold": [5, 5, 5, 6, 6],
                       "silver": [5, 5, 5, 5, 5],
                       "leather": [1, 1, 1, 1, 1, 1, 2, 3, 4],
                       "cloth": [1, 1, 2, 2, 3, 3, 5],
                       "spice": [1, 1, 2, 2, 3, 3, 5],
                       "combo3": [1, 1, 2, 2, 2, 3, 3],
                       "combo4": [4, 4, 5, 5, 6, 6],
                       "combo5": [8, 8, 9, 10, 10],
                       "largest_herd": [5],
                       "maharajahs_favourite": [1, 1, 1],
                       }
        # convert values to TokenStacks
        for key, values in self.tokens.items():
            self.tokens[key] = TokenStack(*(Token(key, v) for v in values))
            # shuffle the combo token stacks and sort the others
            if key in ("combo3", "combo4", "combo5"):
                self.tokens[key].shuffle()
            else:
                self.tokens[key].sort_by_value()

        # create deck
        self.deck = Deck()
        self.deck.shuffle()

        # create marketplace/river (always start with 3 camels)
        camels = self.deck.draw_specific("camel", 3)
        rest = self.deck.draw(2)
        self.marketplace = Marketplace(camels + rest)

        # create players
        pass

        # deal player hands
        pass

game = Game()
mp = game.marketplace
#deck = Deck()
#deck.shuffle()
#token = Token("diamond", 7)
#diamonds = TokenStack(*(Token("diamond", value) for value in [7, 7, 5, 5, 5]))
#leather_tokens = (Token("leather", value) for value in [4, 3, 2, 1, 1, 1, 1])
#leather = TokenStack(*leather_tokens)
#gold = TokenStack(*[Token("gold", value) for value in [6, 6, 5, 5, 5]])
#silver = TokenStack(Token("silver", 5), Token("silver", 5), Token("silver", 5))
#print(f"diamond stack = {diamonds.get_values()}")
#diamonds.sort_by_value()
#print(f"diamond stack = {diamonds.get_values()}")
