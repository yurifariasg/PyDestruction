import Map
from Bomberman import *
import pygame
import Physics

class Game(object):

    def __init__(self, screen):
        self.map = Map.Map() # Number of Players
        self.physics = Physics.Physics(self.map)
        self.screen = screen
    
    def start_game(self):
        
        ## Add Players
        
        # Default Images (Temporary)
        lista_passE3 = [pygame.image.load("imagens/esquerdapasso1jonata.png"),
                        pygame.image.load("imagens/esquerdapasso2jonata.png"),
                        pygame.image.load("imagens/paradoesquerdajonata.png")]
        lista_passD3 = [pygame.image.load("imagens/direitapasso1jonata.png"),
                        pygame.image.load("imagens/paradodireitajonata.png"),
                        pygame.image.load("imagens/direitapasso2jonata.png")]
        lista_passC3 = [pygame.image.load("imagens/cimapasso1jonata.png"),
                        pygame.image.load("imagens/paradocimajonata.png"),
                        pygame.image.load("imagens/cimapasso2jonata.png")]
        lista_passB3 = [pygame.image.load("imagens/frentepasso1jonata.png"),
                        pygame.image.load("imagens/paradofrentejonata.png"),
                        pygame.image.load("imagens/frentepasso2jonata.png")]
        paradoFrente3 = pygame.image.load("imagens/paradofrentejonata.png").convert_alpha()
        paradoEsquerda3 = pygame.image.load("imagens/paradoesquerdajonata.png").convert_alpha()
        paradoDireita3 = pygame.image.load("imagens/paradodireitajonata.png").convert_alpha()
        paradoCima3 = pygame.image.load("imagens/paradocimajonata.png").convert_alpha()
        
        animation_images = {
                            'IDLE' : {
                                      'UP' : [paradoCima3],
                                      'RIGHT' : [paradoDireita3],
                                      'LEFT' : [paradoEsquerda3],
                                      'DOWN' : [paradoFrente3]},
                            'MOVING' : {
                                      'UP' : lista_passC3,
                                      'RIGHT' : lista_passD3,
                                      'LEFT' : lista_passE3,
                                      'DOWN' : lista_passB3}}
        
        self.map.players.append(
                                Bomberman('Player 1',
                                          {'bombs' : 1,
                                           'lives' : 1,
                                           'speed' : 1,
                                           'range' : 1},
                                          (0, 0),
                                          animation_images))
        
        self.map.players.append(
                                Bomberman('Player 2',
                                          {'bombs' : 1,
                                           'lives' : 1,
                                           'speed' : 1,
                                           'range' : 1},
                                          (0, 0),
                                          animation_images))
        self.map.init() # Initialize Our Map
        
        previous_pressed_keys = {}
        
        self.is_running = True
        
        while self.is_running: # screen.fill(tema_background)
            
            self.screen.fill(Settings.BACKGROUND) # Clear Screen
            
            # Step 1: Get Input
            for e in pygame.event.get():
                if e.type == pygame.QUIT or (e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE):
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
                    self.map.players[0].place_bomb(self.map)
                previous_pressed_keys[pygame.K_SPACE] = True
            else:
                previous_pressed_keys[pygame.K_SPACE] = False
            
            # Step 2: Do Physics
            
            self.physics.update()
            
            # Step 3: Render
            
            self.map.render(self.screen)
            
            pygame.display.flip()
            
        
        # Quit