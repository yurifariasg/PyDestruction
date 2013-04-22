import pygame
import Settings
import time
import PowerUP

class Direction(object):
    LEFT = 'LEFT'
    RIGHT = 'RIGHT'
    UP = 'UP'
    DOWN = 'DOWN'

class Bomberman(object):

    def __init__(self, name, initial_data, initial_pos, animation_images):
        
        self.name = name
        self.rect = pygame.Rect(initial_pos[0], initial_pos[1],
                                Settings.BOMBERMAN_SIZE, Settings.BOMBERMAN_SIZE)
        self.invulnerable = False
        self.time_invulnerable = 0
        self.is_visible = True
        self.time_image_blink = 0
        self.animation_images = animation_images
        self.initial_status = {'bombs' : initial_data.get('bombs', 1),
                               'lives' : initial_data.get('lives', 1),
                               'speed' : initial_data.get('speed', 1),
                               'range' : initial_data.get('range', 1)}
        self.current_status = self.initial_status
        self.current_bombs = self.current_status['bombs']
        
        self.direction = Direction.DOWN
        self.is_moving = False
        self.animation_time = 0
        
        self.speed_x = 0
        self.speed_y = 0
    
    def movement(self, direction):
        if direction == Direction.DOWN:
            self.speed_y = self.current_status.get('speed') * Settings.DEFAULT_SPEED
        if direction == Direction.UP:
            self.speed_y = - self.current_status.get('speed') * Settings.DEFAULT_SPEED
        if direction == Direction.RIGHT:
            self.speed_x = self.current_status.get('speed') * Settings.DEFAULT_SPEED
        if direction == Direction.LEFT:
            self.speed_x = - self.current_status.get('speed') * Settings.DEFAULT_SPEED
        self.direction = direction
        self.is_moving = True
    
    def take_power(self, powerup):
        for key, value in powerup.items():
            if self.current_status.get(key) != None:
                self.current_status[key] = self.current_status[key] + value
    
    def drop_power(self):
        powerup = PowerUP.PowerUP()
        powerup.attributes['bombs'] = self.current_status['bombs'] - self.initial_status['bombs']
        powerup.attributes['speed'] = self.current_status['speed'] - self.initial_status['speed']
        powerup.attributes['range'] = self.current_status['range'] - self.initial_status['range']
        return powerup
    
    def take_damage(self):
        self.current_status['lives'] = self.current_status['lives'] - 1
        self.invulnerable = True
        self.time_invulnerable = time.time() + Settings.INVULNERABLE_TIME
        self.is_visible = False
        self.time_image_blink = time.time()
        
    
    def is_dead(self):
        return self.current_status['lives'] <= 0
    
    def render(self, screen):
        image = None
        if self.is_moving:
            if time.time() - self.animation_time > 0.3 / self.current_status.get('speed'): # Animation
                self.animation_images['MOVING'][self.direction] = \
                        self.shift(self.animation_images['MOVING'][self.direction])
                self.animation_time = time.time()
                
            image = self.animation_images['MOVING'][self.direction][0]
            self.is_moving = False
        else:
            if time.time() - self.animation_time > 0.3 / self.current_status.get('speed'): # Animation
                self.animation_images['IDLE'][self.direction] = \
                        self.shift(self.animation_images['IDLE'][self.direction])
                self.animation_time = time.time()
                
            image = self.animation_images['IDLE'][self.direction][0]
        
        
        if self.invulnerable:
            if time.time() - self.time_image_blink > Settings.TIME_BETWEEN_BLINKING:
                self.is_visible = not self.is_visible
                self.time_image_blink = time.time()
            
            if time.time() - self.time_invulnerable > 0:
                self.invulnerable = False
                self.is_visible = True
        else:
            self.is_visible = True
                
        if self.is_visible:
            screen.blit(image, pygame.Rect(self.rect.x - 8,
                                                        self.rect.y - 30,
                                                        13,
                                                        13))
        
    def shift(self, list): # Does a left shift on the given list
        return list[1:] + [list[0]]