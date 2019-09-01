import random
import round as rnd

class Player:
    
    def __init__(self, id):
        self.new_round()
        self.id = id
        
    def deal_hand(self, deck):
        self.hand = deck.deal_cards(self, 25)
        
    def sort_hand(self):
        return 1
        
    def get_id(self):
        return self.id
    
    def get_card_num(self, i):
        return self.hand[i].card_in_num()
    
    def get_cards_left(self):
        return len(self.hand)
    
    def is_card_selected(self, i):
        return i in self.selected_cards_indices
    
    def append_selected_cards(self, i):
        if not i in self.selected_cards_indices:
            self.selected_cards_indices.append(i)
        else:
            self.selected_cards_indices.remove(i)
            
    def reset_selected_cards(self):
        self.selected_cards_indices = []
        
    def get_selected_cards_in_hand(self):
        return [self.hand[i] for i in self.selected_cards_indices]
    
    def get_selected_cards_in_indices(self):
        return self.selected_cards_indices
    
    def get_selected_cards_in_num(self):
        return [self.hand[index].card_in_num() for index in self.selected_cards_indices]
        
    def give_points(self, points):
        self.points += points
        
    def get_points(self):
        return self.points
    
    def played_cards(self):
        for i in self.get_selected_cards_in_indices():
            self.hand.pop(i)
        
        self.reset_selected_cards()
            
    def new_round(self):
        self.points = 0
        self.lord = False
        self.selected_cards_indices = [] #by index
        self.hand = []
    
    def ai_play(self, r, game, players):
        self.reset_selected_cards()
        self.ai_choice(r, game, players)
    
    # Shit way - do it randomly    
    def ai_choice(self, r, game, players):
        limit = self.get_cards_left()
        self.reset_selected_cards()
        if r.get_num_played() == 0:
            self.selected_cards_indices.append(random.randint(0, limit - 1))
        else:
            num = len(r.played[(self.get_id() - 1) % 4])
            tries = 0
            while(not r.is_valid_move(game, players)):
                tries += 1
                if tries == 1000:
                    print("help, ai stuck")
                    print(self.selected_cards_indices)
                    break
                self.reset_selected_cards()
                for i in range(num):
                    self.selected_cards_indices.append(random.randint(0, limit - 1))
                    
                self.selected_cards_indices = list(set(self.selected_cards_indices))
                