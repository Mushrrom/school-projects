import pygame

import src.main.game as game

from src.consts import *

# pygame setup
pygame.init()
pygame.display.set_caption("SpaceWar!2")
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

gameLoop = True
while gameLoop:
    src.menus.mainMenu.renderMenu(screen)
    
    # src.main.game.gameLoop(screen)

pygame.quit()