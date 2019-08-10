# implements game logic
"""
Game setup
    Determine (number of) players
        (name)
        (id)
    Setup playing field
        Deal nobles from nobles_deck
            = number of players +1
        Deal development cards
            Deal 4 level 1 development cards
            Deal 4 level 2 development cards
            Deal 4 level 3 development cards
        Setup gems
            4 players: 7, 7, 7, 7, 7, 5
            3 players: 5, 5, 5, 5, 5, 5
            2 players: 4, 4, 4, 4, 4, 5

Turn (for each player)
    Do an action
    Get noble (if applicable)
    Win (if applicable)
    Check if player qualifies for a noble

Possible Turn actions
    * Take 3 different gems
        Only if available, not gold
        Discard gems down to a total of 10
    * Take 2 identical gems
        Only if available
        Discard gems down to a total of 10
    * Reserve development card
        Only if less than 3 development cards currently reserved
        Gain 1 gold (if available)
        Discard gems down to a total of 10
    * Play development card
        Either on field or in own reserved development cards

# keep track of turns
"""

from abc import ABC
import random
from typing import List
from dataclasses import dataclass
import json


class BrilliantGame():

    # players
    # deck_level_1
    # deck_level_2
    # deck_level_3

    def __init__(self, number_of_players):
        # check if number of players is at least 2
        self.number_of_players = number_of_players
        print(f"Starting game with {self.number_of_players} players.")

        # don't hardcode stuff in here...
        self.players = [Player('Alice'), Player('Bob'), Player('Chris')]
        self.deck1 = DevelopmentDeck(
            None, 'development_cards.json', {'level': 1})
        self.deck2 = DevelopmentDeck(
            None, 'development_cards.json', {'level': 2})
        self.deck3 = DevelopmentDeck(
            None, 'development_cards.json', {'level': 3})
        self.deckn = NoblesDeck(None, 'nobles_cards.json')
        self.field = Field(self)

    def debug(self):
        # print('Players:')
        # print([p.render() for p in self.players])
        print('Deck 1: [' + ', '.join([str(self.deck1[i]['id'])
                                       for i in range(4)]) + ']')
        print('Deck 2: [' + ', '.join([str(self.deck2[i]['id'])
                                       for i in range(4)]) + ']')
        print('Deck 3: [' + ', '.join([str(self.deck3[i]['id'])
                                       for i in range(4)]) + ']')
        print('Nobles deck: [' + ', '.join([str(self.deckn[i]['name'])
                                            for i in range(self.number_of_players + 1)]) + ']')
        print('Field:')
        print(self.field.gems)
        print(' fields_level_1' + str([c['id']
                                       for c in self.field.cards_level_1]))
        print(' fields_level_2' + str([c['id']
                                       for c in self.field.cards_level_2]))
        print(' fields_level_3' + str([c['id']
                                       for c in self.field.cards_level_3]))


class Player():

    # gamestate_important
        # points
            # update at end of turn
    # utility
        # is

    def __init__(self, name):
        self.name = name
        self.gems = GemStack()
        self.development_cards = []
        self.reserved_development_cards = []
        self.nobles_cards = []

    def render(self):  # / to_json
        # returns playerstate
        # pass
        return self.__dict__
        #return {'name': self.name}


class Card(ABC):
    """ Abstract card representation.
        Implements:
            File loading
            Rendering
    """

    def load_json(self, json_file):
        with open(json_file) as jf:
            self.__init__(**json.load(jf))


# @dataclass
# class DevelopmentCard(Card):
#     '''Represents a development card.'''
#     id: int  # 1-90
#     level: int  # 1, 2, 3
#     cost_diamond: int  # 0-7
#     cost_sapphire: int  # 0-7
#     cost_emerald: int  # 0-7
#     cost_ruby: int  # 0-7
#     cost_onyx: int  # 0-7
#     points_value: int  # 0-7
#     # could also use indexOf... with int... { diamond, sapphire, emerald, ruby, onyx }
#     provides: str
#     image_file: str = "blank.png"  # default to blank for rendering simply


# @dataclass
# class NobleCard(Card):
#     '''Represents a noble card.'''
#     id: int
#     name: str
#     cost_white: int
#     cost_blue: int
#     cost_green: int
#     cost_red: int
#     cost_black: int
#     points_value: int
#     image_file: str


class Deck(ABC):

    def __init__(self, cards: List[Card] = [], json_file=None, f=None):
        """ Either load cards from an existing list of DevelopmentCards or,
            from a json datafile (json_file) and then apply the required filter (f)
        """
        if cards:
            self.cards = cards
        else:
            self.cards = []
        if json_file:
            self.load_json(json_file)
        if f:
            for k, v in f.items():
                setattr(self, k, v)
                self.cards = list(filter(lambda c: c[k] == v, self.cards))
        # self.shuffle()

    def load_json(self, json_file):
        with open(json_file) as jf:
            self.__init__(**json.load(jf))

    def __str__(self):
        return f'{[c for c in self.cards]}'

    def __getitem__(self, key):
        # try?
        return self.cards[key]

    def draw(self):
        # basically just pop(), can add other triggers...
        try:
            return self.cards.pop()
        except IndexError:
            # no more cards in deck
            return None

    def shuffle(self):
        random.shuffle(self.cards)
        # just shuffle... use predictable rng for testing?


class DevelopmentDeck(Deck):
    '''Stores a stack of development cards'''


class NoblesDeck(Deck):
    '''Stores a stack of development cards'''


class Field():
    """ Keeps track of the playing field data"""

    gem_rules = {
        2: [4, 4, 4, 4, 4, 5],
        3: [5, 5, 5, 5, 5, 5],
        4: [7, 7, 7, 7, 7, 5],
    }
    card_names = {
        1: 'cards_level_1',
        2: 'cards_level_2',
        3: 'cards_level_3',
    }

    def __init__(self, game):
        self.game = game
        self.gems = GemStack(*self.gem_rules[game.number_of_players])
        self.cards_level_1 = [game.deck1.draw() for i in range(4)]
        self.cards_level_2 = [game.deck2.draw() for i in range(4)]
        self.cards_level_3 = [game.deck3.draw() for i in range(4)]
        self.nobles = [game.deckn.draw()
                       for i in range(game.number_of_players + 1)]

    # don't really need this... pass field to player
    # def pick_card(self, index):
    #     pass


@dataclass
class GemStack:
    """ Inventory of gems for players or playing field
        Setup gems
            4 players: 7, 7, 7, 7, 7, 5
            3 players: 5, 5, 5, 5, 5, 5
            2 players: 4, 4, 4, 4, 4, 5
    """

    diamond: int = 0
    sapphire: int = 0
    emerald: int = 0
    ruby: int = 0
    onyx: int = 0
    gold: int = 0

    def render():
        return self.__dict__
