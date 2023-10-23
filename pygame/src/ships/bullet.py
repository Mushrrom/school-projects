import math

import pygame
from src.consts import *

class newBullet():
    def __init__(self, startPos, speed, angle, origin):
        """bullet

        Args:
            startX (int): Starting X of bullet
            startY (int): Starting Y of bullet
            speed (int|float): Speed of bulle
            direction (int|float): Direction the bullet will be traveling in
            origin (str): Origin of the bullet (Can be "player" or "enemy") to prevent friendly fire
        """
        self.position = startPos
        self.angle = angle
        self.speed = speed
        self.origin = origin
        self.distance = 0

        image = pygame.transform.scale_by(pygame.image.load("assets/bullet.png"), 3)
        self.image = pygame.transform.rotate(image, angle)

        self.rect = image.get_rect()

    def checkCollisions(self, player, enemiesList):
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
        self.distance += 1
        # get x and y distances
        xDist = -1*math.sin(self.angle*math.pi/180)*self.speed
        yDist = -1*math.cos(self.angle*math.pi/180)*self.speed

        # add that to the position
        self.position[0] += xDist
        self.position[1] += yDist

        self.rect = self.rect = self.image.get_rect(center = self.image.get_rect(center = (self.position[0], self.position[1])).center)

    def render(self, screen):
        screen.blit(self.image, self.rect)

    def clearBullet(self, screen):
        pygame.draw.rect(screen, CLEAR, (self.position[0]-10, self.position[1]-10, 20, 20))