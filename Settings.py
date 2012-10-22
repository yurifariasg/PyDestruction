import pygame

'''
    Settings File
'''

BLOCK_SIZE = 32
BOMBERMAN_SIZE = 16
DEFAULT_SPEED = 1

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
BACKGROUND = (0,120,0)