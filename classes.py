
from random import shuffle

class Deck():
    """This class represents the deck of goods cards from which the marketplace
    cards are drawn. It is similar to a stack, but I've added the option to
    draw multiple cards at a time, and shuffle the order.
    """
    def __init__(self, diamond=6, silver=6, gold=6, silk=8, spices=8,
                 leather=10):
        cards = (["diamond"] * diamond
                 + ["silver"] * silver
                 + ["gold"] * gold
                 + ["silk"] * silk
                 + ["spices"] * spices
                 + ["leather"] * leather)
        print(cards)
        self.cards = list(cards)  # cards should be a list

    def shuffle(self):
        shuffle(self.cards)

    def draw(self, number_of_cards=1):
        return [self.cards.pop() for __ in range(number_of_cards)]

    def peek(self, number_of_cards=1):
        return self.cards[-number_of_cards:]

    def __len__(self):
        return len(self.cards)

    def __repr__(self):
        return str(self.cards)


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
        return f"{self.name} token worth {self.value} points"

class Marketplace():
    """Represents the 5 card river marketplace.
    Needs to keep track of empty spaces and/or preserve the order
    def __init__(self):
        pass



deck = Deck()
print(deck)
deck.shuffle()
print(deck)
token = Token("diamond", 7)
print(token)
