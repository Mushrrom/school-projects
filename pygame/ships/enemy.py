import math

import pygame

import mathFunctions

class newEnemy:
    def __init__(self):
        self.position = [0, 0]
        self.image = pygame.transform.scale_by(pygame.image.load("enemy.png"), 2)
        self.rect = self.image.get_rect()
        self.angle = 0

    def moveEnemy(self, distance):
        """_summary_

        Args:
            distance (float/int): distance to move

        Returns:
            _type_: _description_
        """

        # Calculates the distance (*math.pi/180) converts from degrees to radians
        # and its multiplied by -1 because it goes the wrong way if you don't
        xDist = -1*math.sin(self.angle*math.pi/180)*distance
        yDist = -1*math.cos(self.angle*math.pi/180)*distance

        self.position[0] += xDist
        self.position[1] += yDist


    def renderEnemy(self, screen):
        rotatedImage = pygame.transform.rotate(self.image, self.angle)
        self.rect = rotatedImage.get_rect(center = self.image.get_rect(center = (self.position[0], self.position[1])).center)

        # self.rect.move_ip(self.position[0], self.position[1])

        screen.blit(rotatedImage, self.rect)

    def rotateEnemy(self, playerX, playerY):
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

        # print(angleToPlayer)
        # print(self.angle)

        if relativeAngle > 0:
            self.angle += 5
        elif relativeAngle < 0:
            self.angle -= 5

        if self.angle < 0:
            self.angle += 360
        if self.angle > 360:
            self.angle -= 360


