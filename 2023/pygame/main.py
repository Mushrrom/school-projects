import pygame

from src.consts import *
import src.menus.mainMenu
import src.menus.highScore

# pygame setup
pygame.init()
pygame.display.set_caption("SpaceWar!2")
pygame.freetype.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

import src.main.game as game

gameLoop = True
while gameLoop:
    option = src.menus.mainMenu.renderMenu(screen)

    if option == 0:
        src.main.game.gameLoop(screen)
    elif option == 1:
        src.menus.highScore.showHighScores(screen)
    elif option == 2:
        gameLoop = False

pygame.quit()