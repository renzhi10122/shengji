import random

class Card:
    suits = ["hearts", "diamonds", "clubs", "spades"]
    ranks = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
    
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.actual_suit = suit
        
    def get_rank(self):
        return self.rank
    
    def get_ordered_rank(self): #so this puts A as 14
        if self.rank == 1:
            return 14
        return self.rank
    
    def get_suit(self):
        return self.suit
    
    def get_actual_suit(self):
        return self.actual_suit
    
    def set_actual_suit(self, trump_rank, trump_suit):
        if self.rank == trump_rank or self.rank > 13:
            self.actual_suit = trump_suit
    
    @staticmethod
    def get_rank_from_num(num):
        return (((num - (num % 4)) / 4) % 13) + 1
    
    @staticmethod
    def get_suit_from_num(num):
        if num >= 52:
            return 4
        
        return num % 4
    
    @staticmethod
    def get_actual_suit_from_num(num, trump_suit, trump_rank):
        suit = Card.get_suit_from_num(num)
        rank = Card.get_rank_from_num(num)
        if suit == 4 or rank == trump_rank:
            return trump_suit
        
        return suit
    
    # print out card in a string
    def card_in_words(self):
        if self.suit == 4:
            if self.rank == 0:
                return "Black joker"
            else:
                return "Red joker"
            
        return self.ranks[self.rank - 1] + " of " + self.suits[self.suit]
    
    def card_in_num(self):
        if self.suit == 4:
            return 38 + self.rank
        
        return (self.rank-1)  * 4 + self.suit
        

class Deck:
    def __init__(self, num_of_decks = 1, shuffle = True, jokers = True):
        self.cards = []
        
        for i in range(1, num_of_decks + 1):
            for suit in range(0,4):
                for rank in range(1,14):
                    self.cards.append(Card(suit, rank))
                    
        if jokers:
            self.cards.append(Card(4, 14))
            self.cards.append(Card(4, 15))
        
        if shuffle:        
            self.shuffle()
    
    # print out each card in a string
    def deck_in_words(self):
        for card in self.cards:
            card.card_in_words()
            
    def shuffle(self):
        random.shuffle(self.cards)
        
    def count(self):
        return len(self.cards)
    
    def deal_cards(self, player, num_of_cards = 1):
        hand = []
        for i in range(num_of_cards):
            hand.append(self.cards.pop())
        
        return hand

