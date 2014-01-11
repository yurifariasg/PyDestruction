import pygame

'''
    Settings File
'''

BLOCK_SIZE = 32
BOMBERMAN_SIZE = 16
DEFAULT_SPEED = 1
INVULNERABLE_TIME = 3
TIME_BETWEEN_BLINKING = 0.2
DESTRUCTIBLE_BLOCKS_COUNT = 100
MINIMUM_TIME_PER_FRAME = 0.025

MAP = [
    "ZZZZZZZZZZZZZZZZZZZZZZZZZ",
    "Z                       Z",
    "Z W W W W W W W W W W W Z",
    "Z                       Z",
    "Z W W W W W W W W W W W Z",
    "Z                       Z",
    "Z W W W W W W W W W W W Z",
    "Z                       Z",
    "Z W W W W W W W W W W W Z",
    "Z                       Z",
    "Z W W W W W W W W W W W Z",
    "Z                       Z",
    "Z W W W W W W W W W W W Z",
    "Z                       Z",
    "Z W W W W W W W W W W W Z",
    "Z                       Z",
    "ZZZZZZZZZZZZZZZZZZZZZZZZZ",
    ]

DEFAULT_DESTRUCTABLE_BLOCK_IMAGE = "imagens/cenario/cone2.jpg"
DEFAULT_BORDER_BLOCK_IMAGE = "imagens/cenario/cone.jpg"
DEFAULT_FIXED_BLOCKS_IMAGE = "imagens/cenario/cone.jpg"
FIRE_HORIZONTAL_LEFT_EDGE_PATH = "imagens/fire_esq.png"
FIRE_HORIZONTAL_RIGHT_EDGE_PATH = "imagens/fire_dir.png"
FIRE_HORIZONTAL_PATH = "imagens/fire_horizontal.png"
FIRE_CENTER_PATH = "imagens/fire_centro.png"
FIRE_VERTICAL_TOP_EDGE_PATH = "imagens/fire_cima.png"
FIRE_VERTICAL_BOTTOM_EDGE_PATH = "imagens/fire_baix.png"
FIRE_VERTICAL_PATH = "imagens/fire_vertical.png"

DEFAULT_FONT_PATH = "fonts/Chonker.ttf"



BOMB_ANIMATION = ["imagens/bomb3.png", "imagens/bomb2.png", "imagens/bomb.png"]
BACKGROUND = (0,120,0)