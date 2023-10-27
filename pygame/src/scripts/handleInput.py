import pygame
from pygame.locals import *


class inputHandler():
    """Class for handling inputs

    Attributes:
        keyUp (bool): Whether the key up is currently pressed.
        keyDown (bool): Whether the key down is currently pressed.
        keyLeft (bool): Whether the key left is currently pressed.
        keyRight (bool): Whether the key right is currently pressed.

    """
    def __init__(self):
        self.keyLeft = False
        self.keyRight = False
        self.keyUp = False
        self.keyDown = False

    def handleInput(self):
        """Handles what keys have been pressed

        Returns:
            bool: gameloop is whether to keep running the game, the rest are the current values of
                the keys
        """
        gameLoop = True
        keyC = False
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
                elif event.key == K_c:
                    keyC = True


            elif event.type == KEYUP:
                if event.key == K_LEFT:
                    self.keyLeft = False
                elif event.key == K_RIGHT:
                    self.keyRight = False
                elif event.key == K_UP:
                    self.keyUp = False
                elif event.key == K_DOWN:
                    self.keyDown = False

        return gameLoop, self.keyUp, self.keyDown, self.keyLeft, self.keyRight, keyC
