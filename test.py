'''
import deck
import player
import round
import game

player1 = player.Player(0)
player2 = player.Player(1)
player3 = player.Player(2)
player4 = player.Player(3)
players = [player1, player2, player3, player4]
d = deck.Deck(2)
g = game.Game(2, 0, 0)

c1 = deck.Card(0, 1)
c2 = deck.Card(0, 13)
c3 = deck.Card(0, 1)
c4 = deck.Card(0, 13)
c5 = deck.Card(0, 2)
c6 = deck.Card(0, 2)
c7 = deck.Card(1, 2)
c8 = deck.Card(1, 2)
c7.set_actual_suit(2, 0)
c8.set_actual_suit(2, 0)
print(round.Round.assign_rank(g, c8))

hand = [c1, c2, c3, c4, c5, c6, c7, c8]
print(round.Round.categorize(g, hand))
'''

a = [1,2,3]

def thing(a):
    a = a + [4]

thing(a)
print(a)