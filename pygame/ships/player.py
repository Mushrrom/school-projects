import pygame
import math


class newPlayer():
    def __init__(self):
        # player values for amount to move
        self.rotationAmount = 0
        self.speed = 0

        # player values for position
        self.position = [250, 250]
        self.angle = 0

        # image + rect
        self.img = pygame.transform.scale_by(pygame.image.load("test_image.png"), 2)
        self.rect = self.img.get_rect()

        # debug
        print(f"DEBUG: center = {self.rect.center}")

    def updateMovement(self, keyUp, keyDown, keyLeft, keyRight):
        if keyLeft == True:
            # if self.rotationAmount < 1:
            #     self.rotationAmount += 0.4
            # else:
            #     self.rotationAmount += 0.1
            self.angle += 7

        if keyRight == True:
            # if self.rotationAmount > -1:
            #     self.rotationAmount -= 0.4
            # else:
            #     self.rotationAmount -= 0.1
            self.angle -= 7

        if keyUp == True:
            self.speed += 0.15 if self.speed < 40 else 0

        if keyDown == True:
            self.speed -= 0.15
            self.speed = max(self.speed, 0)

    def move(self):
        self.angle += self.rotationAmount

        xDist = -1*math.sin(self.angle*math.pi/180)*self.speed
        yDist = -1*math.cos(self.angle*math.pi/180)*self.speed

        self.position[0] += xDist
        self.position[1] += yDist

        if self.position[0] > 640:
            self.position[0] = 0
        elif self.position[0] < 0:
            self.position[0] = 640

        if self.position[1] > 480:
            self.position[1] = 0
        elif self.position[1] < 0:
            self.position[1] = 480

    def render(self, screen):
        rotatedImage = pygame.transform.rotate(self.img, self.angle)

        self.rect = rotatedImage.get_rect(center = self.img.get_rect(center = (self.position[0], self.position[1])).center)
        screen.blit(rotatedImage, self.rect)
