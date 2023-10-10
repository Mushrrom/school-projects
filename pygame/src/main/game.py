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

    surface = pygame.Surface((10000, 10000)).convert_alpha()

    while playing:
        screen.fill(BG)
        surface.fill(CLEAR)
        [playing, keyUp, keyDown, keyLeft, keyRight] = inputHandler.handleInput()

        # TODO:
        # [ ] Move this to its own function and iterate through them

        newEnemy.rotateEnemy(player.position[0], player.position[1])
        newEnemy.moveEnemy(6)
        newEnemy.renderEnemy(surface)

        newEnemy2.rotateEnemy(player.position[0], player.position[1])
        newEnemy2.moveEnemy(6)
        newEnemy2.renderEnemy(surface)

        for i in range(100):
            for j in range(100):
                if i*100
                pygame.draw.rect(surface, (255, 255,255), (i*100, j*100, 10, 10))

        screen.blit(surface, (-(player.position[0]-SCREEN_WIDTH//2), -(player.position[1]-SCREEN_HEIGHT//2)))

        player.updateMovement(keyUp, keyDown, keyLeft, keyRight)
        player.move()
        player.render(screen)

        GAME_FONT.render_to(screen, (0, 0), f"fps: {round(clock.get_fps())}", (0, 0, 0))
        pygame.display.update()

        clock.tick(FPS)
