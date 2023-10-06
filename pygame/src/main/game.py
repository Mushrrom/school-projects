import pygame
import pygame.freetype
import src.scripts.handleInput
from src.ships import enemy, player

from src.consts import *

def gameLoop(screen):
    # ANCHOR - other setup
    inputHandler = src.scripts.handleInput.inputHandler()
    player = src.ships.player.newPlayer()

    playing = True

    clock = pygame.time.Clock()

    GAME_FONT = pygame.freetype.Font("assets/bauhaus.ttf", 24)

    # ships (debug for now)
    newEnemy = src.ships.enemy.newEnemy()
    newEnemy2 = src.ships.enemy.newEnemy(pos=[250, 250])

    while playing:
        screen.fill(BG)

        [playing, keyUp, keyDown, keyLeft, keyRight] = inputHandler.handleInput()

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
