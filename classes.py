from random import shuffle

class Deck():
    """This class represents the deck of goods cards from which the marketplace
    cards are drawn. It is similar to a stack, but I've added the option to
    draw multiple cards at a time, and shuffle the order.
    """
    def __init__(self, diamond=6, silver=6, gold=6, silk=8, spices=8,
                 leather=10, camel=15):
        contents = (["diamond"] * diamond
                 + ["silver"] * silver
                 + ["gold"] * gold
                 + ["silk"] * silk
                 + ["spices"] * spices
                 + ["leather"] * leather
                 + ["camel"] * camel)
        self.contents = list(contents)  # contents should be a list

    def shuffle(self):
        shuffle(self.contents)

    def draw(self, number=1):
        return [self.contents.pop() for __ in range(number)]

    def peek(self, depth=1):
        return self.contents[-depth:]

    def __len__(self):
        return len(self.contents)

    def __repr__(self):
        return str(self.contents)


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


class TokenStack(Deck):
    """Represents the stacks of tokens. Could be anything from the market goods
    to the Biggest Herd token to the combo tokens.
    Functionally very similar to the Deck class, but not limited to the card
    types
    """
    def __init__(self, *list_of_tokens):
        self.contents = list(list_of_tokens)

    def sort_by_value(self, descending=True):
        """Sort the stack of tokens so that the highest value ones are on top.
        This means the highest value tokens should be the first to get popped
        off the list---meaning they should be at the end of the list.
        """
        self.contents = sorted(self.contents, key=lambda x: x.value)

    def get_values(self):
        return [token.value for token in self.contents]


class Marketplace():
    """Represents the 5 card river marketplace.
    Needs to keep track of empty spaces and/or preserve the order.
    """
    def __init__(self):
        pass


#def initialise_game():
#    # create deck
#    # create marketplace/river
#    # create token piles


deck = Deck()
deck.shuffle()
token = Token("diamond", 7)
diamonds = TokenStack(*(Token("diamond", value) for value in [7, 7, 5, 5, 5]))
leather_tokens = (Token("leather", value) for value in [4, 3, 2, 1, 1, 1, 1])
leather = TokenStack(*leather_tokens)
gold = TokenStack(*[Token("gold", value) for value in [6, 6, 5, 5, 5]])
silver = TokenStack(Token("silver", 5), Token("silver", 5), Token("silver", 5))
print(f"diamond stack = {diamonds.get_values()}")
diamonds.sort_by_value()
print(f"diamond stack = {diamonds.get_values()}")
