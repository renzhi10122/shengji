import pygame

import deck as d
import player
import round as rd

from pygame.locals import *
# point cards - 5 - 17,18,19,20
#               10- 37,38,39,40
#               K - 49,50,51,52
# H - 1,5,...
# D - 2,6,...
# C - 3,7,...
# S - 4,8,...

# Add dealing
# Add is_valid_move details
# Add jokers
# Add sorting

class Game:
    #
    def __init__(self, trump_rank, trump_suit, lord):
        self.trump_rank = trump_rank
        self.trump_suit = trump_suit
        self.lord = lord
        self.ended = False
        self.play_first = lord
        self.points = [0] * 4
            
    def get_trump_suit(self):
        return self.trump_suit
            
    def get_trump_rank(self):
        return self.trump_rank
    
    def get_ended(self):
        return self.ended
    
    def get_lord(self):
        return self.lord
    
    def get_play_first(self):
        return self.play_first
    
    def set_play_first(self, winner):
        self.play_first = winner
    
    def is_ended(self):
        return self.ended
    
    def end(self):
        self.ended = True
        
class App:
    def __init__(self):
        self._running = True
        self._display_surf = None
        self.size = self.weight, self.height = 760, 760
 
    def on_init(self):
        pygame.init()
        pygame.font.init()
        self.screen = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self._running = True
        self.card_images = [0] * 52
        self.font = pygame.font.SysFont('Comic Sans MS', 12)
        for i in range(1, 14):
            self.card_images[4*i - 4] = pygame.image.load("png/" + str(i) + "_H.png")
            self.card_images[4*i - 3] = pygame.image.load("png/" + str(i) + "_D.png")
            self.card_images[4*i - 2] = pygame.image.load("png/" + str(i) + "_C.png")
            self.card_images[4*i - 1] = pygame.image.load("png/" + str(i) + "_S.png")
            self.card_images[4*i - 4] = pygame.transform.scale(self.card_images[4*i - 4], (80, 122))
            self.card_images[4*i - 3] = pygame.transform.scale(self.card_images[4*i - 3], (80, 122))
            self.card_images[4*i - 2] = pygame.transform.scale(self.card_images[4*i - 2], (80, 122))
            self.card_images[4*i - 1] = pygame.transform.scale(self.card_images[4*i - 1], (80, 122))
            
        self.card_images.append(pygame.image.load("png/B.png"))
        self.card_images.append(pygame.image.load("png/R.png"))
        self.card_images[52] = pygame.transform.scale(self.card_images[52], (80, 122))
        self.card_images[53] = pygame.transform.scale(self.card_images[53], (80, 122))
        self.card_images.append(pygame.image.load("png/red_back.png"))
        self.card_images[54] = pygame.transform.scale(self.card_images[54], (80, 122))
        self.play_button = pygame.image.load("png/play_button.png")
 
    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            if pos[1] >= 600 and pos[1] <= 722:
                x_coord = pos[0] - ((pos[0] + 10) % 20) + 10
                x_coord = int(x_coord / 20 - 1)
                if self.players[0].get_cards_left() > x_coord:
                    self.players[0].append_selected_cards(x_coord)
                    
                self.on_render()
            if pos[1] >= 620 and pos[1] <= 670 and pos[0] >= 600 and pos[0] <= 690:      
                return True
        
        return False
            
    def on_loop(self):
        pass
    def on_render(self):
        pygame.draw.rect(self.screen, (0,0,0), (10, 560, 560, 162))
        pygame.draw.rect(self.screen, (0,0,0), (0, 0, 560, 20))
        self.screen.blit(self.play_button, (600, 620))
        textsurface = self.font.render(str(self.players[0].get_points()), False, (255, 255, 255))
        self.screen.blit(textsurface, (0, 0))
        for i in range(self.players[0].get_cards_left()):
            if self.players[0].is_card_selected(i):
                self.screen.blit(self.card_images[self.players[0].get_card_num(i)],(10 + 20*i,560))
            else:
                self.screen.blit(self.card_images[self.players[0].get_card_num(i)],(10 + 20*i,600))
        pygame.display.flip()
        
    def on_cleanup(self):
        pygame.quit()
 
    def on_execute(self):
        if self.on_init() == False:
            self._running = False
            
        player1 = player.Player(0)
        player2 = player.Player(1)
        player3 = player.Player(2)
        player4 = player.Player(3)
        self.players = [player1, player2, player3, player4]
        self.deck = d.Deck(2)
        #add dealing here
        for i in range(4):
            self.players[i].deal_hand(self.deck)
        #
        trump_rank = 2
        trump_suit = 0
        for card in self.deck.cards:
            card.set_actual_suit(trump_suit, trump_rank)
            
        lord = 0
        self.on_render()
        while(self._running):
            self.play_game(trump_rank, trump_suit, lord)
            
        self.on_cleanup()

    def play_game(self, trump_rank, trump_suit, lord):
        game = Game(trump_rank, trump_suit, lord)
        while(not game.is_ended() and self._running):
            r = rd.Round(game.get_play_first())
            while(not r.is_ended() and self._running):
                player = self.players[r.get_current_player()]
                
                while(r.get_current_player() == 0 and 
                      not r.has_player_selected() and 
                      self._running):
                    for event in pygame.event.get():
                        if self.on_event(event):
                            r.has_selected()
                # Try to play and update Round vars, else retry
                if r.get_current_player() > 0:
                    player.ai_play(r, game)
                    
                if r.play(self.players, game):
                    self.draw_play(r)
                    player.played_cards() # update all player variables
                    r.next_player()
                else: #not valid
                    player.reset_selected_cards()  
                    r.reset_selected()
                    
                pygame.draw.rect(self.screen, (0,0,0), (0, 0, 560, 100))
                textsurface = self.font.render(str(self.players[0].get_points()), False, (255, 255, 255))
                self.screen.blit(textsurface, (0, 0))
                textsurface = self.font.render(str(r.get_points()), False, (255, 255, 255))
                self.screen.blit(textsurface, (0, 20))
                pygame.display.flip()
                pygame.time.wait(1000)
                self.on_render()
                
                if r.get_num_played() == 4:
                    winner = r.highest(game)
                    print("highest is " + str(winner))
                    self.players[winner].give_points(r.get_points())
                    game.set_play_first(winner)
                    r.end()
            
            if self.players[0].get_cards_left() <= 0:
                game.end()
                return 0
                
    def draw_play(self, r):
        player = r.get_current_player()
        played = r.played[r.get_current_player()]
        x = 0
        y = 0
        if player == 0:
            x = 400
            y = 400
        elif player == 1:
            x = 500
            y = 300
        elif player == 2:
            x = 400
            y = 200
        elif player == 3:
            x = 300
            y = 300
        print(played)
        for index, i in enumerate(played):
            self.screen.blit(self.card_images[i], (x + 20 * index, y))
        
        pygame.display.flip()
            
if __name__ == "__main__" :
    theApp = App()
    theApp.on_execute()