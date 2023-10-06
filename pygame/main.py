import pygame
from pygame.locals import *
import pygame.freetype

import src.scripts.handleInput
import src.scripts.mathFunctions

import src.ships.enemy
import src.ships.player

# pygame setup
pygame.init()
pygame.display.set_caption("test game")
clock = pygame.time.Clock()

# ANCHOR - other setup
inputHandler = handleInput.inputHandler()
player = ships.player.newPlayer()

# consts
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
FPS = 60
BG = 127, 127, 0
GAME_FONT = pygame.freetype.Font("assets/bauhaus.ttf", 24)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

gameLoop = True

# ships (debug for now)
newEnemy = ships.enemy.newEnemy()
newEnemy2 = ships.enemy.newEnemy(pos=[250, 250])

# keys:
keyLeft = False
keyRight = False
keyUp = False
keyDown = False

#ANCHOR - game

while gameLoop:
    screen.fill(BG)
    [gameLoop, keyUp, keyDown, keyLeft, keyRight] = inputHandler.handleInput()

    player.updateMovement(keyUp, keyDown, keyLeft, keyRight)
    player.move()
    player.render(screen)

    newEnemy.rotateEnemy(player.position[0], player.position[1])
    newEnemy.moveEnemy(6)
    newEnemy.renderEnemy(screen)

    newEnemy2.rotateEnemy(player.position[0], player.position[1])
    newEnemy2.moveEnemy(6)
    newEnemy2.renderEnemy(screen)

    # playerX += newPos[0]
    # playerY += newPos[1]

    GAME_FONT.render_to(screen, (0, 0), f"fps: {round(clock.get_fps())}", (0, 0, 0))
    pygame.display.update()

    clock.tick(FPS)


pygame.quit()

