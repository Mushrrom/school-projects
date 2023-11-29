import pygame.freetype as _freetype
_freetype.init()
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
FPS = 60
BG = 0, 0, 0
CLEAR = 0, 0, 0, 0
GAME_FONT = _freetype.Font("assets/PixelifySans-Regular.ttf", 24)