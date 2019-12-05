from random import shuffle


allowed_token_names = ("diamond", "silver", "gold", "cloth", "spice",
                       "leather", "combo3", "combo4", "combo5", "largest_herd",
                       )


class Token():
    """Represents the round goods tokens which give players points. Each token
    should have
    - a value (on the back)
    - the name (on the front) e.g. "diamond" or "triple combo"
    """

    def __init__(self, name, value):
        if name not in allowed_token_names:
            raise ValueError(f"{name} is not a legal token name.")
        if value <= 0:
            raise ValueError("Illegal token value (zero or negative)")
        if not isinstance(value, int):
            raise ValueError("Illegal token value (non-integer)")
        self.name = name
        self.value = value

    def __repr__(self):
        return str(self.value)


class Deck(list):
    def __init__(self, default=False, **kwargs):
        # default deck for Jaipur
        if default:
            contents = {"diamond": 6,
                        "gold": 6,
                        "silver": 6,
                        "cloth": 8,
                        "spice": 8,
                        "leather": 10,
                        "camel": 11}
        else:
            contents = {}
        # update with any specific requests from kwargs
        contents.update(kwargs)
        # convert to list
        temp = []
        for goods, amount in contents.items():
            temp.extend([goods] * amount)
        super().__init__(temp)

    def shuffle(self):
        shuffle(self)

    def draw(self, number=1):
        """Draw the next card(s)"""
        drawn_cards = []
        try:
            for __ in range(number):
                drawn_cards.append(self.pop())
        except IndexError:
            pass
        finally:
            return drawn_cards

    def take(self, card, number=1):
        """Take a card by name"""
        return [self.pop(self.index(card)) for __ in range(number)]

    def peek(self, depth=1):
        """Look at the next card(s)"""
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


class Marketplace(Deck):
    """Represents the 5 card river marketplace.
    Needs to keep track of empty spaces and/or preserve the order.
    """
    def __init__(self, list_of_5_cards):
        super().__init__()
        self.extend(list_of_5_cards)

    def swap(self, player_card, market_card):
        """Swap one player card for one market card. Illegal move. Intended for
        use as part of the trade() method."""
        # remove market card
        ind = self.index(market_card)
        out, = self.take(market_card)  # comma because only ever one card
        self.insert(ind, player_card)  # insert player card into same slot
        return out

    def trade(self, player_cards, market_cards):
        """Swap several player cards for several marketplace cards"""
        # start swapping
        out = []
        for player_card, market_card in zip(player_cards, market_cards):
            out.append(self.swap(player_card, market_card))
        return out

    def take_camels(self):
        return self.take("camel", self.count("camel"))


class Player():
    def __init__(self, name):
        self.name = name
        self.hand = Deck()
        self.tokens = []
        self.victory_points = 0
        self.herd = Deck()


class Game():
    def __init__(self):
        """Setup actions at the very beginning of the game"""
        # create players
        self.player1 = Player(name="Player 1")
        self.player2 = Player(name="Player 2")
        self.players = self.player1, self.player2
        self.current_player = 0

    def setup_round(self):
        """Setup actions at the start of each round"""
        # create token piles
        # populate tokens dictionary
        self.resource_tokens = {"diamond": [5, 5, 5, 7, 7],
                                "gold": [5, 5, 5, 6, 6],
                                "silver": [5, 5, 5, 5, 5],
                                "leather": [1, 1, 1, 1, 1, 1, 2, 3, 4],
                                "cloth": [1, 1, 2, 2, 3, 3, 5],
                                "spice": [1, 1, 2, 2, 3, 3, 5],
                                }
        self.bonus_tokens = {"combo3": [1, 1, 2, 2, 2, 3, 3],
                             "combo4": [4, 4, 5, 5, 6, 6],
                             "combo5": [8, 8, 9, 10, 10],
                             }

        # convert values to TokenStacks
        for key, values in self.resource_tokens.items():
            self.resource_tokens[key] = TokenStack(*(Token(key, v) for v in values))
            self.resource_tokens[key].sort_by_value()
        for key, values in self.bonus_tokens.items():
            self.bonus_tokens[key] = TokenStack(*(Token(key, v) for v in values))
            self.bonus_tokens[key].shuffle()

        # create deck
        self.deck = Deck(default=True)
        self.deck.shuffle()

        # create marketplace/river (always start with 3 camels)
        camels = self.deck.take("camel", 3)
        rest = self.deck.draw(2)
        self.marketplace = Marketplace(camels + rest)

        # setup players
        for player in self.players:
#            player.hand.extend(self.deck.draw(4))  # deal player hands
            # move camels from hand to herd
            if "camel" in player.hand:
                N = player.hand.count("camel")
                player.herd.extend(player.hand.take("camel", N))
            player.tokens = []                     # reset player tokens

    def check_for_game_over(self):
        # has the market run out of cards?
        if len(self.deck) == 0:
            return True
        # are three or more resource tokens depleted?
        stack_lengths = [len(stack) for stack in self.resource_tokens.values()]
        if stack_lengths.count(0) >= 3:
            return True
        return False

    def prompt_player_turn(self, player):
        message = (f"{player.name}, it is your turn. \n"
                   "Do one of the following:\n"
                   "\t1) 'buy diamond' --> take 1 diamond from the market\n"
                   "\t2) 'trade leather camel for diamond gold' --> trade your leather & camel for gold & diamond\n"
                   "\t3) 'sell cloth' --> sell all your cloth. You can specify a number to sell: 'sell 2 cloth'\n"
                   "\t4) 'camels' --> take all the camels\n"
                   )
        inp = input(prompt=message).strip()
        if inp == "camels":
            return inp,

        action, inp = inp.split(" ", maxsplit=1)

        if action == "buy":
            goods = inp.strip()  # the rest of the string is the goods name
            return action, goods
        elif action == "trade":
            player_cards, market_cards = inp.split("for")
            # use regexp to detect "2 camel 1 spice" or "camel camel spice"
            # maybe start with the latter and then add the regexp functionality
            # later
            player_cards = player_cards.strip().split(" ")
            market_cards = market_cards.strip().split(" ")
            return action, player_cards, market_cards
        elif action == "sell":
            goods = inp.strip().split(" ")
            if len(goods) > 1:  # if the player has specified number of goods
                goods, amount = goods
                amount = int(amount)
            else:
                goods, = goods
                amount = "all"
            return action, goods, amount
        else:
            raise Exception("unrecognised action!")

    def refill_marketplace(self):
        while len(self.marketplace) < 5:
            self.marketplace.extend(self.deck.draw())
            if len(self.deck) == 0:
                break

    def buy(self, player, card):
        # take card from marketplace into player hand
        player.hand.extend(self.marketplace.take(card))
        self.refill_marketplace()

    def sell(self, player, goods, amount):
        # resolve amount (int vs. "all")
        if amount == "all":
            amount = player.hand.count(goods)
        # remove the cards from the player's hand
        player.hand.take(goods, amount)
        # take tokens from the token pile and add to player tokens
        player.tokens.extend(self.resource_tokens[goods].draw(amount))

    def trade(self, player, player_cards, market_cards):
        # take the cards out of the player's hand (or herd, if camel)
        for card in player_cards:
            if card == "camel":
                player.herd.take(card)
            else:
                player.hand.take(card)
        # do the market trade
        self.marketplace.trade(player_cards, market_cards)
        # place market cards in player hand
        player.hand.extend(market_cards)

    def take_camels(self, player):
        player.herd.extend(self.marketplace.take_camels())
        self.refill_marketplace()

    def player_turn(self):
        # get current player
        player = self.players[self.current_player % 2]

        # prompt player for action
        response = self.prompt_player_turn(player)
        if response[0] == "buy":
            action, goods = response
            # check player hand size.
            if len(player.hand) >= 7:
                return ("You already have 7 cards in your hand. "
                        "You can't buy.")
            # you can't buy a camel
            if goods == "camel":
                return ("You can't buy a camel. Use the 'camels' action "
                        "instead.")
            self.buy(player, goods)
            return True  # turn satisfactorily resolved
        if response[0] == "trade":
            action, player_cards, market_cards = response
            # check if trade is possible
            if len(player_cards) != len(market_cards):
                return ("The number of player cards doesn't match the "
                        "number of market cards for trade.")
            if len(player_cards) == 1:
                return ("You can't trade less than 2 cards.")
            if "camel" in market_cards:
                return ("You can't trade for camels in the market")
            # check if the requested market_cards are all there
            counts = {card: market_cards.count(card) for card in market_cards}
            for card, amount in counts.items():
                if self.marketplace.count(card) < amount:
                    return (f"There are not enough {card} cards in the "
                            "marketplace for this trade")
            # check hand size
            non_camel_cards = [c for c in player_cards if c != "camel"]
            if len(player.hand) - len(non_camel_cards) + len(market_cards) > 7:
                raise Exception("Your hand will be greater than 7 cards after "
                                "this trade")

            self.trade(player, player_cards, market_cards)
            return True
        if response[0] == "sell":
            action, goods, amount = response
            self.sell(player, goods, amount)
            return True
        if response[0] == "camels":
            if self.marketplace.count("camel") == 0:
                return ("There are no camels in the marketplace. Try another "
                        "action.")
            self.take_camels(player)
            return True

    def play_round(self):
        self.setup_round()
        while self.check_for_game_over is not True:
            response = ""
            while response is not True:
                print(self)  # print the board
                if response:
                    print(">"*90+"\n"+response+"\n"+">"*90)
                response = self.player_turn()  # play out player turn
            self.current_player += 1  # increment current player

        # after round has finished,
        # award the largest herd token
        player1_herd_size = len(self.player1.herd)
        player2_herd_size = len(self.player2.herd)
        if player1_herd_size > player2_herd_size:
            player1.tokens.append(Token("largest_herd", 5))

        # count token points
        player1_points = sum(token.value for token in self.player1.tokens)
        player2_points = sum(token.value for token in self.player2.tokens)

        # award victory points
        if player1_points > player2_points:
            self.player1.victory_points += 1
            return f"{self.player1.name} wins this round."
        elif player1_points < player2_points:
            self.player2.victory_points += 1
            return f"{self.player2.name} wins this round."
        else:
            self.player1.victory_points += 1
            self.player2.victory_points += 1
            return f"It's a draw! Both players get a victory point."

    def play_game(self):
        print("ROUND 1!")
        self.play_round()
        print("ROUND 2!")
        self.play_round()
        for player in self.players:
            if player.victory_points == 2:
                print(f"THE WINNER IS {player.name.upper()}!")
                return None
        print("ROUND 3!")
        self.play_round()
        for player in self.players:
            if player.victory_points == 2:
                print(f"THE WINNER IS {player.name.upper()}!")
                return None

    def __repr__(self):
        diamond = "{:<10}".format("diamond:")+"{:<20}".format(str(game.resource_tokens["diamond"]))
        gold = "{:<10}".format("gold:")+"{:<20}".format(str(game.resource_tokens["gold"]))
        silver = "{:<10}".format("silver:")+"{:<20}".format(str(game.resource_tokens["silver"]))
        spice = "{:<10}".format("spice:")+"{:<20}".format(str(game.resource_tokens["spice"]))
        cloth = "{:<10}".format("cloth:")+"{:<20}".format(str(game.resource_tokens["cloth"]))
        leather = "{:<10}".format("leather:")+"{:<20}".format(str(game.resource_tokens["leather"]))

        strings = ["="*90,
                   f"{self.player1.name}",
                   f"\thand: {self.player1.hand}",
                   f"\ttokens: {self.player1.tokens}",
                   f"\therd: {len(self.player1.herd)}",
                   f"MARKETPLACE: {self.marketplace}",
                   "TOKENS:",
                   "\t"+diamond, "\t"+gold, "\t"+silver, "\t"+spice,
                   "\t"+cloth, "\t"+leather,
                   f"{self.player2.name}",
                   f"\thand: {self.player2.hand}",
                   f"\ttokens: {self.player2.tokens}",
                   f"\therd: {len(self.player2.herd)}",
                   ]
        return "\n".join(strings)

game = Game()
game.play_game()

""" TODO:
    - implement take_camels method for game.
    - merge actions from Marketplace into Game class
    - take starting camels from player hand to herd
    - enforce hand size for players
    - sort player hand in game print
    - enforce 2 sale minimum sale for d, g, s
    - implement combo reward tokens
    """