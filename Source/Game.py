import Map
from Bomberman import *
import pygame
import Physics
from time import time
from Enemy import *

class GameState(object):
    GAME_RUNNING = 0
    PLAYER_VICTORY = 1
    BOT_VICTORY = 2
    MENU = 3

class Game(object):

    def __init__(self, screen):
        self.map = Map.Map()
        self.physics = Physics.Physics(self.map)
        self.screen = screen
        self.last_frame_time = 0
        self.font = pygame.font.SysFont(Settings.DEFAULT_FONT_PATH, 35)
        self.font_big = pygame.font.SysFont(Settings.DEFAULT_FONT_PATH, 60)
    
    def start_game(self):
        
        ## Add Players
        
        # Default Images (Temporary)
        lista_passE2 = [pygame.image.load("imagens/esquerdapasso1otacilio.png"),
                        pygame.image.load("imagens/esquerdapasso2otacilio.png"),
                        pygame.image.load("imagens/paradoesquerdaotacilio.png")]
        lista_passD2 = [pygame.image.load("imagens/direitapasso1otacilio.png"),
                        pygame.image.load("imagens/paradodireitaotacilio.png"),
                        pygame.image.load("imagens/direitapasso2otacilio.png")]
        lista_passC2 = [pygame.image.load("imagens/cimapasso1otacilio.png"),
                        pygame.image.load("imagens/paradocimaotacilio.png"),
                        pygame.image.load("imagens/cimapasso2otacilio.png")]
        lista_passB2 = [pygame.image.load("imagens/frentepasso1otacilio.png"),
                        pygame.image.load("imagens/paradofrenteotacilio.png"),
                        pygame.image.load("imagens/frentepasso2otacilio.png")]
        parado_frente2 = pygame.image.load("imagens/paradofrenteotacilio.png").convert_alpha()
        parado_esquerda2 = pygame.image.load("imagens/paradoesquerdaotacilio.png").convert_alpha()
        parado_direita2 = pygame.image.load("imagens/paradodireitaotacilio.png").convert_alpha()
        parado_cima2 = pygame.image.load("imagens/paradocimaotacilio.png").convert_alpha()
        
        lista_passE3 = [pygame.image.load("imagens/esquerdapasso1jorge.png"),
                        pygame.image.load("imagens/esquerdapasso2jorge.png"),
                        pygame.image.load("imagens/paradoesquerdajorge.png")]
        lista_passD3 = [pygame.image.load("imagens/direitapasso1jorge.png"),
                        pygame.image.load("imagens/paradodireitajorge.png"),
                        pygame.image.load("imagens/direitapasso2jorge.png")]
        lista_passC3 = [pygame.image.load("imagens/cimapasso1jorge.png"),
                        pygame.image.load("imagens/paradocimajorge.png"),
                        pygame.image.load("imagens/cimapasso2jorge.png")]
        lista_passB3 = [pygame.image.load("imagens/frentepasso1jorge.png"),
                        pygame.image.load("imagens/paradofrentejorge.png"),
                        pygame.image.load("imagens/frentepasso2jorge.png")]
        parado_frente3 = pygame.image.load("imagens/paradofrentejorge.png").convert_alpha()
        parado_esquerda3 = pygame.image.load("imagens/paradoesquerdajorge.png").convert_alpha()
        parado_direita3 = pygame.image.load("imagens/paradodireitajorge.png").convert_alpha()
        parado_cima3 = pygame.image.load("imagens/paradocimajorge.png").convert_alpha()
        
        animation_images2 = {
                            'IDLE' : {
                                      'UP' : [parado_cima2],
                                      'RIGHT' : [parado_direita2],
                                      'LEFT' : [parado_esquerda2],
                                      'DOWN' : [parado_frente2]},
                            'MOVING' : {
                                      'UP' : lista_passC2,
                                      'RIGHT' : lista_passD2,
                                      'LEFT' : lista_passE2,
                                      'DOWN' : lista_passB2}}
        
        animation_images3 = {
                            'IDLE' : {
                                      'UP' : [parado_cima3],
                                      'RIGHT' : [parado_direita3],
                                      'LEFT' : [parado_esquerda3],
                                      'DOWN' : [parado_frente3]},
                            'MOVING' : {
                                      'UP' : lista_passC3,
                                      'RIGHT' : lista_passD3,
                                      'LEFT' : lista_passE3,
                                      'DOWN' : lista_passB3}}
        
        self.map.players.append(
                                Bomberman.Bomberman('Player 1',
                                          {'bombs' : 1,
                                           'lives' : 2,
                                           'speed' : 5,
                                           'range' : 5},
                                          (0, 0),
                                          animation_images2))
        
        self.map.players.append(
                                Enemy('Bot',
                                          {'bombs' : 1,
                                           'lives' : 2,
                                           'speed' : 5,
                                           'range' : 4},
                                          (0, 0),
                                          animation_images3))
        
        ### Load Status Bar Stuff
        self.status_bar = pygame.image.load("imagens/powerups/barra_status.png").convert_alpha()
        #self.font = pygame.font.SysFont("Chonker.tff", 22)
        #self.font_big = pygame.font.SysFont("Chonker.tff", 65)
        #self.font_medium = pygame.font.SysFont("Chonker.tff", 30)
        
        
        self.map.init() # Initialize Our Map
        
        self.is_running = True
        self.currentState = GameState.GAME_RUNNING
        
        while self.is_running:
            
            if self.currentState == GameState.GAME_RUNNING:
                self.executeGame()
            elif self.currentState == GameState.PLAYER_VICTORY:
                self.playerVictoryScreen()
            elif self.currentState == GameState.BOT_VICTORY:
                self.botVictoryScreen()
    
    def playerVictoryScreen(self):
        bg = pygame.image.load("screens/player_victory.png")
        start_time = time()
        hasEnded = False
        
        while time() - start_time < 5 and not hasEnded:
            self.screen.fill(Settings.BACKGROUND)
            for e in pygame.event.get():
                if e.type == pygame.QUIT or (e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE):
                    hasEnded = True
            self.screen.blit(bg, pygame.Rect(0, 0, 1024, 800))
            pygame.display.flip()
        self.is_running = False
            
    def botVictoryScreen(self):
        bg = pygame.image.load("screens/player_defeat.png")
        start_time = time()
        hasEnded = False
        
        while time() - start_time < 5 and not hasEnded:
            self.screen.fill(Settings.BACKGROUND)
            for e in pygame.event.get():
                if e.type == pygame.QUIT or (e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE):
                    hasEnded = True
            self.screen.blit(bg, pygame.Rect(0, 0, 1024, 800))
            pygame.display.flip()
        self.is_running = False
    
    def executeGame(self):
        has_ended = False
        previous_pressed_keys = {}
        self.start_time = time()
        while not has_ended:
            self.screen.fill(Settings.BACKGROUND) # Clear Screen
            
            # Check Victory State
            if self.map.players[0].current_status.get('lives') <= 0:
                has_ended = True
                self.currentState = GameState.BOT_VICTORY
            elif self.map.players[1].current_status.get('lives') <= 0:
                has_ended = True
                self.currentState = GameState.PLAYER_VICTORY
            
            # Step 1: Get Input
            for e in pygame.event.get():
                if e.type == pygame.QUIT or (e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE):
                    has_ended = True
                    self.is_running = False
                    
            key = pygame.key.get_pressed()
            if key[pygame.K_UP]:
                self.map.players[0].movement(Direction.UP)
            if key[pygame.K_DOWN]:
                self.map.players[0].movement(Direction.DOWN)
            if key[pygame.K_LEFT]:
                self.map.players[0].movement(Direction.LEFT)
            if key[pygame.K_RIGHT]:
                self.map.players[0].movement(Direction.RIGHT)
            
            if key[pygame.K_SPACE]:
                if not previous_pressed_keys.get(pygame.K_SPACE):
                    self.map.add_player_bomb(self.map.players[0])
                previous_pressed_keys[pygame.K_SPACE] = True
            else:
                previous_pressed_keys[pygame.K_SPACE] = False
            
            if time() - self.last_frame_time > Settings.MINIMUM_TIME_PER_FRAME:
                self.last_frame_time = time() # Wait for Frame
                
                # Step 2: Update Bots
                self.map.update_bots()
                
                # Step 3: Do Physics
                self.physics.update()
            
            # Step 4: Render
            self.map.render(self.screen)
            self.renderStatusBar(self.screen)
            pygame.display.flip()
    
    def renderStatusBar(self, screen):
        # Stats UI
        screen.blit(self.status_bar,(0,543))

        # Stats Player 1
        bombs1 = self.font.render(str(self.map.players[0].current_status.get('bombs')), 1, (255,255,255))
        life1 = self.font.render(str(self.map.players[0].current_status.get('lives')), 1, (255,255,255))
        speed1 = self.font.render(str(self.map.players[0].current_status.get('speed')), 1, (255,255,255))
        range1 = self.font.render(str(self.map.players[0].current_status.get('range')), 1, (255,255,255))

        screen.blit(range1, (53,576))
        screen.blit(life1, (122,576))
        screen.blit(speed1, (190,576))
        screen.blit(bombs1, (259,576))
        
        # Stats Player 2
        bombs2 = self.font.render(str(self.map.players[1].current_status.get('bombs')), 1, (255,255,255))
        life2 = self.font.render(str(self.map.players[1].current_status.get('lives')), 1, (255,255,255))
        speed2 = self.font.render(str(self.map.players[1].current_status.get('speed')), 1, (255,255,255))
        range2 = self.font.render(str(self.map.players[1].current_status.get('range')), 1, (255,255,255))

        screen.blit(range2, (538,576))
        screen.blit(life2, (607,576))
        screen.blit(speed2, (675,576))
        screen.blit(bombs2, (744,576))
        
        # Time

        time_text = self.font_big.render(self.getFormatedTime(), 1, (255,255,255))
        
        screen.blit(time_text, (355,550))
        
    def getFormatedTime(self):
        current = time() - self.start_time
        return "%02d:%02d" % (current / 60, current % 60) 
            