import math
from typing import Union
import pygame
from src.consts import *

class newBullet():
    """Class to represent a player

    Attributes:

        position: (list): Current position of the bullet.
        angle (int): angle of the bullet.
        speed (int): Speed of the bullet -> how many pixels to move the bullet next time movement is
            updated.
        origin (str): The origin of the bullet.
        distance (int): Distance the bullet has traveled (To kill the bullet after it has traveled
            far enough)
    """
    def __init__(self, startPos: list, speed: Union[int, float], angle: int, origin: str):
        self.position = startPos
        self.angle = angle
        self.speed = speed
        self.origin = origin
        self.distance = 0

        image = pygame.transform.scale_by(pygame.image.load("assets/bullet.png"), 3)
        self.image = pygame.transform.rotate(image, angle)

        self.rect = image.get_rect()

    def checkCollisions(self, player, enemiesList: list):
        """Check enemy collisions

        Args:
            player (player): The player object
            enemiesList (list): The list of enemies

        Returns:
            list: index 0 is whether the bullet hit something, and index 1 is what it hit. -1 if
                it hit the player otherwise it returns what enemy it hit
        """
        if self.origin == "enemy":
            if self.rect.colliderect(player.rect):
                player.health -= 10
                return [True, -1]
            else:
                return [False]

        else:
            for count, enemy in enumerate(enemiesList):
                if self.rect.colliderect(enemy.rect):
                    return [True, count]

        return [False]

    def moveBullet(self):
        """Moves the bullet in the direction it is traveling in
        """
        self.distance += 1
        # get x and y distances
        xDist = -1*math.sin(self.angle*math.pi/180)*self.speed
        yDist = -1*math.cos(self.angle*math.pi/180)*self.speed

        # add that to the position
        self.position[0] += xDist
        self.position[1] += yDist

        self.rect = self.rect = self.image.get_rect(center = self.image.get_rect(center = (self.position[0], self.position[1])).center)

    def render(self, screen: pygame.surface):
        """Renders the bullet to a surface at it's current location

        Args:
            screen (pygame.surface): the surface to render the bullet to
        """
        screen.blit(self.image, self.rect)

    def clearBullet(self, screen: pygame.surface):
        """Clears the bullet from a surface (faster than just clearing the entire surface)

        Args:
            screen (pygame.surface): The surface to clear the bullet from
        """
        pygame.draw.rect(screen, CLEAR, (self.position[0]-10, self.position[1]-10, 20, 20))