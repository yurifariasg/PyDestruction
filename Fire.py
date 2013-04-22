import pygame
import Settings
import time

class FireType(object):
    HORIZONTAL_LEFT_EDGE = 0
    HORIZONTAL_RIGHT_EDGE = 1
    HORIZONTAL = 2
    CENTER = 3
    VERTICAL_TOP_EDGE = 4
    VERTICAL_BOTTOM_EDGE = 5
    VERTICAL = 6

class FireState(object):
    ACTIVE = 0
    EXTINGUISHED = 1

class Fire(object):
    IMAGES = [pygame.image.load(Settings.FIRE_HORIZONTAL_LEFT_EDGE_PATH),
              pygame.image.load(Settings.FIRE_HORIZONTAL_RIGHT_EDGE_PATH),
              pygame.image.load(Settings.FIRE_HORIZONTAL_PATH),
              pygame.image.load(Settings.FIRE_CENTER_PATH),
              pygame.image.load(Settings.FIRE_VERTICAL_TOP_EDGE_PATH),
              pygame.image.load(Settings.FIRE_VERTICAL_BOTTOM_EDGE_PATH),
              pygame.image.load(Settings.FIRE_VERTICAL_PATH)]

    def __init__(self, position, type, wall=None):
        self.rect = pygame.Rect(position[0], position[1], Settings.BLOCK_SIZE, Settings.BLOCK_SIZE)
        self.type = type
        self.time_appeared = time.time()
        self.state = FireState.ACTIVE
        self.wall_destroyed = wall
        
    def update(self):
        if self.state == FireState.ACTIVE and time.time() - self.time_appeared > 0.5:
            self.state = FireState.EXTINGUISHED
    
        
    def render(self, screen):
        screen.blit(Fire.IMAGES[self.type], self.rect)
        