import math
from typing import Union

import pygame

from src.consts import *
import src.scripts.functions as mathFunctions

class newEnemy:
    """Class to represent an enemy

    Attributes:
        position: (list): Current position of the enemy.
        angle (int): Current angle of the enemy.
        image (pygame.image): The image of the enemy.
        rect (pygame.Rect): The enemy's rect (Used for collisions).
        frames (int): The amount of frames the enemy has existed for.

    Attributes:
        pos (list): The position to start the enemy at
    """
    def __init__(self, pos: list | None=[0, 0]):


        self.position = pos
        self.angle = 0
        self.image = pygame.transform.scale_by(pygame.image.load("assets/enemy.png"), 3)
        self.rect = self.image.get_rect()


        self.frames = 0 # Amount of frames the enemy has existed for

    def moveEnemy(self, distance: Union[int, float]):
        """_summary_

        Args:
            distance (float, int): distance to move

        Returns:
            _type_: _description_
        """

        # Calculates the distance (*math.pi/180) converts from degrees to radians
        # and its multiplied by -1 because it goes the wrong way if you don't
        xDist = -1*math.sin(self.angle*math.pi/180)*distance
        yDist = -1*math.cos(self.angle*math.pi/180)*distance

        self.position[0] += xDist
        self.position[1] += yDist


    def renderEnemy(self, screen: pygame.surface):
        """Renders the enemy to the enemy surface

        Args:
            screen (pygame.surface): The surface to render the enemy to
        """
        rotatedImage = pygame.transform.rotate(self.image, self.angle)
        self.rect = rotatedImage.get_rect(center = self.image.get_rect(center = (self.position[0], self.position[1])).center)

        # self.rect.move_ip(self.position[0], self.position[1])

        screen.blit(rotatedImage, self.rect)

    def rotateEnemy(self, playerX: Union[int, float], playerY: Union[int, float]):
        """Rotates the enemy towards the player

        Args:
            playerX (int|float): Player x position
            playerY (int|float): Player y position
        """
        angleToPlayer = mathFunctions.getAngle(self.position[0], self.position[1],
                                               playerX, playerY)

        if angleToPlayer < 0:
            angleToPlayer += 360

        relativeAngle = angleToPlayer - self.angle

        if not(-180 < relativeAngle < 180):
                if relativeAngle < -180:
                    relativeAngle += 360
                elif relativeAngle > 180:
                    relativeAngle -= 360


        if relativeAngle > 0:
            self.angle += 5
        elif relativeAngle < 0:
            self.angle -= 5

        if self.angle < 0:
            self.angle += 360
        if self.angle > 360:
            self.angle -= 360

    def clearEnemy(self, screen: pygame.surface):
        self.frames += 1
        """Clears where the enemy used to be on the screen

        Args:
            screen (_type_): _description_
        """
        pygame.draw.rect(screen, CLEAR, (self.position[0]-30, self.position[1]-30, 60, 60))
