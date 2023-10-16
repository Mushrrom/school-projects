import random
import copy

import pygame
import pygame.freetype
import src.scripts.handleInput
from src.ships import enemy, player

from src.consts import *

CLEAR_SURFACE = pygame.Surface((10000, 10000)).convert_alpha()
CLEAR_SURFACE.fill(CLEAR)
def gameLoop(screen):
    # ANCHOR - other setup
    inputHandler = src.scripts.handleInput.inputHandler()
    player = src.ships.player.newPlayer()

    starsSurf = pygame.Surface((10000, 10000)).convert_alpha()
    starsSurf.fill(CLEAR)

    # Debug stars (god is this slow)
    # for i in range(100):
    #     for j in range(100):
    #         pygame.draw.rect(starsSurf, (255, 255,255), (i*100, j*100, 10, 10))

    # Stars for the main stars bg (one that moves with player)
    for _ in range(500_000):
        starX = random.randint(0, 99990)
        starY = random.randint(0, 99990)
        pygame.draw.circle(starsSurf, (255, 255,255), (starX, starY), 4)

    starsSurf2 = pygame.Surface((10000, 10000)).convert_alpha()
    starsSurf2.fill(CLEAR)

    for _ in range(500_000):
        starX = random.randint(0, 99990)
        starY = random.randint(0, 99990)
        pygame.draw.circle(starsSurf2, (180, 180,180), (starX, starY), 2)

    playing = True

    clock = pygame.time.Clock()

    GAME_FONT = pygame.freetype.Font("assets/bauhaus.ttf", 24)

    # ships (debug for now)
    newEnemy = src.ships.enemy.newEnemy()
    newEnemy2 = src.ships.enemy.newEnemy(pos=[250, 250])

    surface = pygame.Surface((10000, 10000)).convert_alpha()
    surface.fill(CLEAR)

    while playing:
        screen.fill(BG)
        [playing, keyUp, keyDown, keyLeft, keyRight] = inputHandler.handleInput()

        # TODO:
        # [ ] Move this to its own function and iterate through them
        surfaceNew = CLEAR_SURFACE
        newEnemy.rotateEnemy(player.position[0], player.position[1])
        newEnemy.moveEnemy(6)
        newEnemy.renderEnemy(surfaceNew)

        newEnemy2.rotateEnemy(player.position[0], player.position[1])
        newEnemy2.moveEnemy(6)
        newEnemy2.renderEnemy(surfaceNew)

        # # Debug stars (god is this slow2)
        # for i in range(100):
        #     for j in range(100):
        #         if player.position[0] - SCREEN_WIDTH//2 - 0 < i*100 < player.position[0]+SCREEN_WIDTH//2 + 0:
        #             if player.position[1] - SCREEN_HEIGHT//2 - 0 < j*100 < player.position[1]+SCREEN_HEIGHT//2 + 0:
        #                 pygame.draw.rect(surface, (255, 255,255), (i*100, j*100, 10, 10))

        GAME_FONT.render_to(screen, (0, 0), f"fps: {round(clock.get_fps())}", (255, 255, 255))
        screen.blit(starsSurf2, (-(player.position[0]//2-SCREEN_WIDTH//2), -(player.position[1]//2-SCREEN_HEIGHT//2)))

        screen.blit(starsSurf, (-(player.position[0]-SCREEN_WIDTH//2), -(player.position[1]-SCREEN_HEIGHT//2)))

        screen.blit(surfaceNew, (-(player.position[0]-SCREEN_WIDTH//2), -(player.position[1]-SCREEN_HEIGHT//2)))

        player.updateMovement(keyUp, keyDown, keyLeft, keyRight)
        player.move()
        player.render(screen)

        pygame.display.update()

        clock.tick(FPS)
