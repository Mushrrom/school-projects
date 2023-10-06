import pygame
from pygame.locals import *


class inputHandler():
    def __init__(self):
        self.keyLeft = False
        self.keyRight = False
        self.keyUp = False
        self.keyDown = False

    def handleInput(self):
        gameLoop = True
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == KEYDOWN:
                if event.key == K_LEFT:
                    self.keyLeft = True
                elif event.key == K_RIGHT:
                    self.keyRight = True
                elif event.key == K_UP:
                    self.keyUp = True
                elif event.key == K_DOWN:
                    self.keyDown = True

            elif event.type == KEYUP:
                if event.key == K_LEFT:
                    self.keyLeft = False
                elif event.key == K_RIGHT:
                    self.keyRight = False
                elif event.key == K_UP:
                    self.keyUp = False
                elif event.key == K_DOWN:
                    self.keyDown = False

        return gameLoop, self.keyUp, self.keyDown, self.keyLeft, self.keyRight
