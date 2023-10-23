import pygame

from src.consts import *
import src.menus.mainMenu
# pygame setup
pygame.init()
pygame.display.set_caption("SpaceWar!2")
pygame.freetype.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

import src.main.game as game

gameLoop = True
while gameLoop:
    option = src.menus.mainMenu.renderMenu(screen)

    if option == "playGame":
        src.main.game.gameLoop(screen)
    elif option == "quit":
        gameLoop = False

pygame.quit()