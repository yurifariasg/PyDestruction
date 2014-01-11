import pygame
import os
import Game

pygame.init()
os.environ["SDL_VIDEO_CENTERED"] = "1"
pygame.display.init()
while not pygame.display.get_init():
    pass
screen = pygame.display.set_mode((800, 600),0,32)
pygame.display.set_caption("PyDestruction - Revamped")
game = Game.Game(screen)

game.start_game()