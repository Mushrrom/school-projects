import random
import time

import pygame
import pygame.freetype
from pygame.locals import *

import src.scripts.handleInput
import src.scripts.highScores
import src.scripts.updateEntities
from src.ships import enemy, player
from src.consts import *


def gameLoop(screen: pygame.surface):
    """The main game loop for the game

    Args:
        screen (pygame.surface): the screen to put the game on
    """
    inputHandler = src.scripts.handleInput.inputHandler()
    player = src.ships.player.newPlayer()
    c_key = pygame.image.load("assets/c_key.png")
    # Render instructions
    screen.fill(BG)
    GAME_FONT.render_to(screen, (100, 100), "How to play: ", (255, 255, 255))
    GAME_FONT.render_to(screen, (100, 200), "Turn ship: left+right key ", (255, 255, 255))
    GAME_FONT.render_to(screen, (100, 250), "Accelerate ship: Up key", (255, 255, 255))
    GAME_FONT.render_to(screen, (100, 300), "Shoot: c", (255, 255, 255))
    GAME_FONT.render_to(screen, (100, 350), "Warp: x", (255, 255, 255))
    GAME_FONT.render_to(screen, (100, 370), "Be careful warping, it has a 1/3 chance", (255, 255, 255))
    GAME_FONT.render_to(screen, (100, 390), "to malfunction and destroy your ship", (255, 255, 255))
    pygame.display.update()

    # starsSurf is the surface of stars that moves with the player
    starsSurf = pygame.Surface((10000, 10000)).convert_alpha()
    starsSurf.fill(CLEAR)

    for _ in range(500_000):
        starX = random.randint(0, 99990)
        starY = random.randint(0, 99990)
        pygame.draw.circle(starsSurf, (255, 255,255), (starX, starY), 4)


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

    # -- Draws the vertical and horizontal walls to the first star surface
    pygame.draw.rect(starsSurf, (127, 127, 127), (0, 0, 20, 10000)) # Left vertical
    pygame.draw.rect(starsSurf, (127, 127, 127), (9_980, 0, 20, 10_000)) # Right vertical

    pygame.draw.rect(starsSurf, (127, 127, 127), (0, 0, 10_000, 20)) # Top horizontal
    pygame.draw.rect(starsSurf, (127, 127, 127), (0, 9_980, 10_000, 20)) # top vertical

    score = 1
    combo = 1
    lastHitTime = 0
    clock = pygame.time.Clock()
    enemiesList = []

    # Surf for enemies and bullets
    enemiesSurface = pygame.Surface((10000, 10000)).convert_alpha()
    enemiesSurface.fill(CLEAR)

    bulletsList = []

    GAME_FONT.render_to(screen, (250, 420), "Continue :", (255, 255, 255))
    screen.blit(c_key, (381, 422))

    pygame.display.update()

    # Wait until c key pressed
    loop = True
    while loop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == KEYDOWN:
                if event.key == K_c:
                    loop = False

        clock.tick(60)

    while playing:
        screen.fill(BG)
        [playing, keyUp, keyDown, keyLeft, keyRight, keyC, keyX] = inputHandler.handleInput()

        bulletsList = src.scripts.updateEntities.updateEnemies(enemiesList, enemiesSurface, player, bulletsList)
        score, combo, lastHitTime = src.scripts.updateEntities.updateBullets(bulletsList, enemiesSurface,
                                                               enemiesList, player, score, combo, lastHitTime)

        timeSinceHit = time.time() - lastHitTime
        if combo > 1:
            if timeSinceHit > 5:
                combo = 1


        if keyC:
            bulletsList.append(player.shootBullet())

        #  -------------------------------
        # / Check collisions with walls /
        # ------------------------------
        if player.position[0]<20:  # Left wall
            # Make player lose health
            player.health -= 20
            # Reset player position to be away from wall
            player.position[0] = 100
            # Make player face away from wall
            player.angle = 270
            # Reset player speed to 0
            player.velocity = [0, 0]
            # Wait 0.5 seconds (one frame @ 2fps)
            clock.tick(2)
        elif player.position[0]>9980:  # Right wall
            player.health -= 20
            player.position[0] = 9900
            player.velocity = [0, 0]
            player.angle = 90
            clock.tick(2)
        elif player.position[1]<20:  # Top wall
            player.health -= 20
            player.position[1] = 100
            player.velocity = [0, 0]
            player.angle = 180
            clock.tick(2)
        elif player.position[1]>9980:  # Bottom wall
            player.health -= 20
            player.position[1] = 9900
            player.speed = 0
            player.velocity = [0, 0]
            clock.tick(2)


        # Spawn new enemies in randomly
        if len(enemiesList) < 5:
            if random.randint(0, 30*len(enemiesList)) == 0:
                enemyX = random.randint(int(player.position[0])-500, int(player.position[0]+500))
                enemyY = random.randint(int(player.position[0]-500), int(player.position[0]+500))
                enemiesList.append(src.ships.enemy.newEnemy(pos=[enemyX, enemyY]))

        if keyX:
            if random.randint(0, 3) == 0:
                playing = False
            else:
                player.position = [random.randint(100, 9900), random.randint(100, 9900)]

        # Update player movement
        player.updateMovement(keyUp, keyDown, keyLeft, keyRight)
        player.move()

        #  -------------------
        # / Rendering stuff /
        # ------------------

        # Render the stars to the screen. Renders the furthest one first and so on
        screen.blit(starsSurf3, (-(player.position[0]//4+SCREEN_WIDTH//2), -(player.position[1]//4+SCREEN_HEIGHT//2)))
        screen.blit(starsSurf2, (-(player.position[0]//2+SCREEN_WIDTH//2), -(player.position[1]//2+SCREEN_HEIGHT//2)))
        screen.blit(starsSurf, (-(player.position[0]-SCREEN_WIDTH//2), -(player.position[1]-SCREEN_HEIGHT//2)))

        # Render the enemies to the screen
        screen.blit(enemiesSurface, (-(player.position[0]-SCREEN_WIDTH//2), -(player.position[1]-SCREEN_HEIGHT//2)))

        # Render the player to the screen
        player.render(screen)

        # Add FPS counter + score + combo to screen
        GAME_FONT.render_to(screen, (0, 10), f"fps: {round(clock.get_fps())}", (255, 255, 255))
        GAME_FONT.render_to(screen, (450, 10), f"score: {score}", (255, 255, 255))

        # Add health bar
        pygame.draw.rect(screen, (255, 0, 0), (110, 450, player.health, 20))
        pygame.draw.rect(screen, (255, 255, 255), (105, 445, 110, 30), 5, 5, 5, 5)
        GAME_FONT.render_to(screen, (10, 450), "health:", (255, 255, 255))

        # Combo amount and countdown
        if combo > 1:
            GAME_FONT.render_to(screen, (500, 450), f"combo: {combo}X", (255, 255, 255))
            pygame.draw.rect(screen, (255, 255, 255), (500, 420, 100-round(timeSinceHit*20), 20))

        # Quit on death
        if player.health <= 0:
            playing = False
        
        pygame.display.update()
        clock.tick(FPS)

    #  ---------------
    # / After death /
    # --------------
    screen.fill(BG)

    GAME_FONT.render_to(screen, (210, 230), f"You died. Score: {score}", (255, 255, 255))
    GAME_FONT.render_to(screen, (250, 300), "Continue :", (255, 255, 255))
    screen.blit(c_key, (381, 302))

    pygame.display.update()

    # Wait until c key pressed
    loop = True
    while loop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == KEYDOWN:
                if event.key == K_c:
                    loop = False

        clock.tick(60)

    src.scripts.highScores.saveHighScore(screen, score, clock)
