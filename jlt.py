from game import DevelopmentDeck, BrilliantGame
# from game import DevelopmentCard
import json

new_game = BrilliantGame(3)
new_game.debug()
# print(new_game.__dict__)
# new_game.deck1.shuffle()
# new_game.deck2.shuffle()
# new_game.deck3.shuffle()
# for i in range(4):
#     print(new_game.deck1.draw()['id'])
# for i in range(4):
#     print(new_game.deck2.draw()['id'])
# for i in range(4):
#     print(new_game.deck3.draw()['id'])
# new_game.deck1.


# c = DevelopmentCard(0, 3, 1, 1, 1, 0, 0, 1, 3)
# print(c)
# c.load_json('development_load_test.json')
# print(c)
# print(dir(c))
# print(c.__str__())

# deck_level_1 = DevelopmentDeck(None, 'development_cards.json', {'level': 1})
# print(deck_level_1)
# deck_level_1.shuffle() #include in init?
# print(deck_level_1)
# for i in range(15):
#     print(deck_level_1.draw())
# deck_level_2 = DevelopmentDeck()
# print(deck_level_2)
# print(deck_level_2.draw())
# deck_level_1.load_json('development_cards.json')

# print(deck_level_1.cards)
# print(deck_level_1)
# deck_level_1.filter('level', 1)
# print(deck_level_1)
