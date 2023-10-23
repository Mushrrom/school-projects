import random
import copy

import pygame
import pygame.freetype
import src.scripts.handleInput
from src.ships import enemy, player
import src.scripts.updateEntities
from src.consts import *

CLEAR_SURFACE = pygame.Surface((10000, 10000)).convert_alpha()
CLEAR_SURFACE.fill(CLEAR)


def gameLoop(screen):
    # ANCHOR - other setup
    inputHandler = src.scripts.handleInput.inputHandler()
    player = src.ships.player.newPlayer()
    # hello
    # starsSurf is the surface of stars that moves with the player
    starsSurf = pygame.Surface((10000, 10000)).convert_alpha()
    starsSurf.fill(CLEAR)

    for _ in range(500_000):
        starX = random.randint(0, 99990)
        starY = random.randint(0, 99990)
        pygame.draw.circle(starsSurf, (255, 255,255), (starX, starY), 4)

    # -- Draws the vertical and horizontal walls to the first star surface
    pygame.draw.rect(starsSurf, (127, 127, 127), (0, 0, 20, 10000)) # Left vertical
    pygame.draw.rect(starsSurf, (127, 127, 127), (9_980, 0, 10_000, 10_000)) # Right vertical

    pygame.draw.rect(starsSurf, (127, 127, 127), (0, 0, 10_000, 20)) # Top horizontal
    pygame.draw.rect(starsSurf, (127, 127, 127), (0, 9_980, 10_000, 10_000)) # top vertical

    # startSurf2 is the surface of the stars that move at 1/2 the speed of the player
    # for the parallax effect
    starsSurf2 = pygame.Surface((10000, 10000)).convert_alpha()
    starsSurf2.fill(CLEAR)

    for _ in range(125_000):
        starX = random.randint(0, 49995)
        starY = random.randint(0, 49995)
        pygame.draw.circle(starsSurf2, (190, 190,190), (starX, starY), 2)


    # startSurf2 is the surface of the stars that move at 1/2 the speed of the player
    # for the parallax effect
    starsSurf3 = pygame.Surface((10000, 10000)).convert_alpha()
    starsSurf3.fill(CLEAR)

    for _ in range(62_500):
        starX = random.randint(0, 24998)
        starY = random.randint(0, 24998)
        pygame.draw.circle(starsSurf3, (150, 150, 150), (starX, starY), 1)
    playing = True

    clock = pygame.time.Clock()

    GAME_FONT = pygame.freetype.Font("assets/bauhaus.ttf", 24)

    # ships (debug for now)
    enemiesList = [src.ships.enemy.newEnemy(), src.ships.enemy.newEnemy(pos=[250, 250])]
    # newEnemy = src.ships.enemy.newEnemy()
    # newEnemy2 = src.ships.enemy.newEnemy(pos=[250, 250])

    enemiesSurface = pygame.Surface((10000, 10000)).convert_alpha()
    enemiesSurface.fill(CLEAR)

    bulletsList = []

    while playing:
        screen.fill(BG)
        [playing, keyUp, keyDown, keyLeft, keyRight] = inputHandler.handleInput()

        # TODO:
        # [X] Move this to its own function and iterate through them

        print(player.health, flush=True)

        bulletsList = src.scripts.updateEntities.updateEnemies(enemiesList, enemiesSurface, player, bulletsList)
        bulletsList = src.scripts.updateEntities.updateBullets(bulletsList, enemiesSurface, enemiesList, player)

        # Render the stars to the screen. Renders the furthest one first and so on
        screen.blit(starsSurf3, (-(player.position[0]//4+SCREEN_WIDTH//2), -(player.position[1]//4+SCREEN_HEIGHT//2)))
        screen.blit(starsSurf2, (-(player.position[0]//2+SCREEN_WIDTH//2), -(player.position[1]//2+SCREEN_HEIGHT//2)))
        screen.blit(starsSurf, (-(player.position[0]-SCREEN_WIDTH//2), -(player.position[1]-SCREEN_HEIGHT//2)))

        # Render the enemies to the screen
        screen.blit(enemiesSurface, (-(player.position[0]-SCREEN_WIDTH//2), -(player.position[1]-SCREEN_HEIGHT//2)))

        # Update player movement and render player to screen
        player.updateMovement(keyUp, keyDown, keyLeft, keyRight)
        player.move()
        player.render(screen)

        # Add FPS counter to screen
        GAME_FONT.render_to(screen, (0, 0), f"fps: {round(clock.get_fps())}", (255, 255, 255))
        pygame.display.update()

        clock.tick(FPS)
