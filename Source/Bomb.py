import Settings
import pygame
import time

class Bomb(object):
    BOMB_IMAGES = [pygame.image.load(image_path)
                   for image_path in Settings.BOMB_ANIMATION] # Load Animation Images

    def __init__(self, colliders, range, timeout_time, rect, owner):
        self.colliders = colliders
        self.range = range
        self.timeout = timeout_time
        self.state = BombState.PLACING
        self.time_placed = time.time()
        self.current_animation = 0
        self.animation_time = 0
        self.rect = rect
        self.owner = owner
        
    def update(self):
        if self.state == BombState.PLACING and not self.isColliding():
            self.state = BombState.PLACED
        
        if time.time() - self.time_placed > self.timeout:
            self.state = BombState.TIMED_OUT
            
        if self.state == BombState.TIMED_OUT and self.owner:
            self.owner.current_status['bombs'] += 1
            self.owner = None # Reset Owner
    
    def isColliding(self):
        for rect in [collider.rect for collider in self.colliders]:
            if self.rect.colliderect(rect):
                return True
        return False
        
    def render(self, screen):
        if time.time() - self.animation_time > 0.2:
            self.current_animation = (self.current_animation + 1) % len(Bomb.BOMB_IMAGES)
            self.animation_time = time.time()
        screen.blit(Bomb.BOMB_IMAGES[self.current_animation], self.rect)

class BombState(object):
    PLACING = 0
    PLACED = 1
    TIMED_OUT = 2