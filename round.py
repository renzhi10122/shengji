from deck import Card

class Round:
    # suit - main suit for the round
    # points - points played in round
    # selected - bool whether or not player has made a move
    # type - single, pair or shuai
    def __init__(self, play_first):
        self.play_first = play_first
        self.current_player = play_first
        self.num_played = 0
        self.played = [0] * 4 # a array of numbers
        self.suit = -1
        self.points = 0
        self.ended = False
        self.selected = False
        self.type = -1
        
    def is_ended(self):
        return self.ended
    
    def get_current_player(self):
        return self.current_player
    
    def next_player(self):
        self.current_player = (self.current_player + 1) % 4
    
    def end(self):
        self.ended = True
    
    def get_suit(self):
        return self.suit
    
    def get_points(self):
        return self.points
    
    def has_selected(self):
        self.selected = True
        
    def reset_selected(self):
        self.selected = False
    
    def get_num_played(self):
        return self.num_played
    
    def inc_num_played(self):
        self.num_played += 1
        
    def has_player_selected(self):
        return self.selected
    
    # For singles and pairs
    # - c1 and c2 both arrays
    # - c1 is assumed to lead
    def higher(self, game, c1, c2):
        card1 = c1[0]
        card2 = c2[0]
        score1 = self.score_card(game, card1)
        score2 = self.score_card(game, card2)
        
        return score1 < score2
            
    def highest(self, game):
        scores = []
        for cards in self.played:
            if self.type == 0 or self.type == 1:
                card = cards[0]
                score = Round.assign_rank(game, card)
                if self.type == 1:
                    if not cards[0] == cards[1]:
                        score -= 1000 # basically, you're screwed
                
                scores.append(score)
                
        winner = 0
        high = 0
        current = self.get_current_player() % 4
        num = 0
        while not num == 4:
            print(scores[current])
            print(current)
            if scores[current] > high:
                winner = current
                high = scores[current]
            
            current = (current + 1) % 4
            num += 1
        
        return winner
    
    def play(self, players, game):
        player = players[self.current_player]
        selected_cards_in_num = player.get_selected_cards_in_num()
        print(selected_cards_in_num)
        if self.is_valid_move(game, players):
            self.played[self.current_player] = selected_cards_in_num
            five_points = [17, 18, 19, 20]
            point_cards = [17, 18 ,19, 20, 37, 38, 39, 40, 49, 50, 51, 52]
            for card in selected_cards_in_num:
                if card in point_cards:
                    if card in five_points:
                        self.points += 5
                    else:
                        self.points += 10    
            
            # If this is the first card in the round
            if self.get_num_played() == 0:
                self.type = 0 if len(selected_cards_in_num) == 1 else 2
                if len(selected_cards_in_num) == 2:
                    if selected_cards_in_num[0] == selected_cards_in_num[1]:
                        self.type = 1
                
                played_card = selected_cards_in_num[0]
                played_rank = player.get_selected_cards_in_hand()[0].get_rank()
                if played_card >= 52 or played_rank == game.get_trump_rank():
                    self.suit = game.get_trump_suit()
                else:
                    self.suit = played_card % 4
                
            self.inc_num_played()
            return True
        else:
            return False
        
    @staticmethod
    def categorize(game, cards): #array of objs
        init = [0] * 18
        types = [init.copy(),init.copy(),init.copy(),init.copy()]
        suits_cards = [[],[],[],[]]
        for card in cards:
            suit = card.get_actual_suit()
            suits_cards[suit].append(card)
        
        for i in range(4):
            suits_cards[i].sort(key = lambda x: Round.assign_rank(game, x))
            ranks = [Round.assign_rank(game, x) for x in suits_cards[i]]
            pairs_in_row = 0
            previous_rank = -1
            while ranks:
                break_row = False
                if len(ranks) > 1 and ranks[0] == ranks[1]:
                    if not previous_rank == -1:
                        current_rank = ranks[0]
                        skip_rank = game.get_trump_rank()
                        dif = 2 if (previous_rank + 1 == skip_rank or 
                                    previous_rank + 1 == skip_rank + 14) else 1
                        if current_rank == previous_rank + dif:
                            pairs_in_row += 1
                            previous_rank = ranks[0]
                            ranks.pop(1)
                            ranks.pop(0)
                        else:
                            break_row = True
                    else:
                        pairs_in_row += 1
                        previous_rank = ranks[0]
                        ranks.pop(1)
                        ranks.pop(0)
                else:
                    ranks.pop(0)
                    types[i][0] += 1
                    types[i][17] += 1
                    break_row = True
                    
                if break_row:
                    types[i][pairs_in_row] += 1
                    types[i][17] += 2 * pairs_in_row
                    pairs_in_row = 0
                    previous_rank = -1
            
            if pairs_in_row > 0:
                types[i][pairs_in_row] += 1
                types[i][17] += 2 * pairs_in_row
   
        return types
        
    @staticmethod
    def assign_rank(game, card): # Card obj
        # Normal cards get rank 2 to 14, A=14 skipping out trump rank
        # then trump cards get 16 to 28 skipping out trump rank
        # then normal trump rank gets 29, trump trump rank gets 30
        # small joker 31, big joker 32
        trump_suit = (card.get_suit() == game.get_trump_suit())
        trump_rank = (card.get_rank() == game.get_trump_rank())
        if card.get_suit() == 4:
            if card.get_rank() == 14:
                return 31
            return 32
        
        if trump_suit:
            if trump_rank:
                return 30
            return card.get_ordered_rank() + 14
        else:
            if trump_rank:
                return 29
            return card.get_ordered_rank()
            
    @staticmethod
    def is_same_suit(cards, trump_suit, trump_rank): # cards is in object Cards
        main_suit = -1
        for card in cards:
            suit = card.get_actual_suit()
            if main_suit == -1:
                main_suit = suit
            else:
                if not suit == main_suit:
                    return False
        
        return True
    
    @staticmethod
    def is_optimised_subsets(t_hand, t_played, t_first):
        pass
            
        
        
    # More logic needed here  
    def is_valid_move(self, game, players): #add logic for playing pairs when you dont have a pair
        player = players[self.current_player]
        selected_cards = player.get_selected_cards_in_hand()
        selected_cards_in_num = player.get_selected_cards_in_num()
        my_hand = player.hand
        if len(my_hand) == 0:
            return False
        #from here we know that the suits are correct
        
        if not self.suit == -1:
            first_played_cards = players[self.play_first].get_selected_cards_in_hand()
            first_types_played = Round.categorize(game, first_played_cards)
            types_played = Round.categorize(game, selected_cards)
            hand_types = Round.categorize(game, my_hand)
            num_to_play = len(first_played_cards)
            if not num_to_play == len(selected_cards):
                return False
            
            #check that you've played the correct number of the suit
            num_of_suit = hand_types[self.suit]['-1']
            actual_of_suit = types_played[self.suit]['-1']
            if not actual_of_suit == min(num_of_suit, num_to_play):
                return False
            # Now the suits and number played have been checked
            # we just need to check if pairs and tractors have been played if needed
            # problems: first played has 1 2_tractor, i only have a 4_tractor
            # first played has 1 2_tractor and 1 4_tractor, i play 2 singles and a 4_tractor
            # first played has 2 4_tractor and 2 3_tractor, i play a 10_tractor and a 5_tractor (greddy doesn't work)
            '''for j in range(4):
                for i in range(16, -1, -1):
                    first = first_types_played[j][str(i)]
                    hand = hand_types[j][str(i)]
                    actual = types_played[j][str(i)]
                    if not min(hand, first) <= actual:
                        return False'''
            for i in range(4):
                if not Round.is_optimised_subsets(hand_types[i], 
                                                  types_played[i], 
                                                  first_types_played[i]):
                    return False
            # So now everything has been checked, done
            return True
        else: #suit == -1
            pass
        if not Round.is_same_suit(my_hand, game.get_trump_suit(), game.get_trump_rank()):
            return False      
            
            
                    
        checked_typ = Round.type_of_play(game, selected_cards)
        if checked_typ == 0:
            if self.type == 0 or self.type == -1:
                return True
            else:
                return False
        
        if checked_typ == 1: #if pair
            if selected_cards_in_num[0] == selected_cards_in_num[1]:
                return True
            else:
                if self.suit == -1:
                    return False
                else:
                    has_pair = False
                    for card1 in my_hand:
                        card_in_num1 = card1.card_in_num()
                        for card2 in my_hand:
                            card_in_num2 = card2.card_in_num()
                            if card_in_num1 == card_in_num2 and card1 != card2:
                                if card1.get_suit() == self.suit:
                                    has_pair == True
                
                    if has_pair:
                        return False
                    else:
                        return True