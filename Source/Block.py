import pygame
import Settings

class Block(object):
    DESTRUCTABLE = 0
    BORDER = 1
    FIXED = 2
    IMAGES = [pygame.image.load(Settings.DEFAULT_DESTRUCTABLE_BLOCK_IMAGE),
              pygame.image.load(Settings.DEFAULT_BORDER_BLOCK_IMAGE),
              pygame.image.load(Settings.DEFAULT_FIXED_BLOCKS_IMAGE)]

    def __init__(self, pos, blockType):
        self.type = blockType
        self.rect = pygame.Rect(pos[0], pos[1], Settings.BLOCK_SIZE, Settings.BLOCK_SIZE)
        self.image = Block.IMAGES[blockType]
        
    @classmethod
    def set_block_images(cls):
        pass
    
    def render(self, screen):
        screen.blit(self.image, self.rect)