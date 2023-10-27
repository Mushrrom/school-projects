import pygame
import math

from src.consts import *

import src.ships.bullet
class newPlayer():
    """Class to represent a player

    Attributes:
        rotationAmount (int): Amount to rotate the player the next time movement is updated.
        speed (int): Speed of the player -> how many pixels to move the player next time movement is
            updated.
        position: (list): Current position of the player.
        angle (int): Current angle of the player.
        img (pygame.image): The image of the player.
        rect (pygame.Rect): The players rect (Used for collisions).
        health (int): The health of the player.
    """
    def __init__(self):
        # player values for amount to move
        self.rotationAmount = 0
        self.speed = 0

        # player values for position
        self.position = [250, 250]
        self.angle = 0

        # image + rect
        self.img = pygame.transform.scale_by(pygame.image.load("assets/test_image.png"), 2)
        self.rect = self.img.get_rect()

        # Health amount
        self.health = 100

        # debug
        print(f"DEBUG: center = {self.rect.center}")

    def updateMovement(self, keyUp: bool, keyDown: bool, keyLeft: bool, keyRight: bool):
        """Updates the player movement

        Args:
            keyUp (bool): Key up currently pressed
            keyDown (bool): Key down currently pressed
            keyLeft (bool): Key left currently pressed
            keyRight (bool): Key right currently pressed
        """
        if keyLeft == True:
            self.angle += 7

        if keyRight == True:
            self.angle -= 7

        if keyUp == True:
            self.speed += 0.15 if self.speed < 40 else 0

        if keyDown == True:
            self.speed -= 0.15
            self.speed = max(self.speed, 0)


    def move(self):
        """Moves the player in the direction it is facing
        """
        # Change angle
        self.angle += self.rotationAmount

        # Calculate how far to move in both directions (this is basically what i was just doing
        # in physics lol)
        xDist = -1*math.sin(self.angle*math.pi/180)*self.speed
        yDist = -1*math.cos(self.angle*math.pi/180)*self.speed

        # add that to the position
        self.position[0] += xDist
        self.position[1] += yDist


    def render(self, screen: pygame.display):
        """Renders the player to the center of the screen

        Args:
            screen (pygame.display): Game screen
        """
        # Rotate player image
        rotatedImage = pygame.transform.rotate(self.img, self.angle)

        # Rect of self for colission calculations
        self.rect = rotatedImage.get_rect(center = self.img.get_rect(center = (self.position[0], self.position[1])).center)

        # Rect that will render to center of screen for what the person sees
        renderRect = rotatedImage.get_rect(center = self.img.get_rect(center = (SCREEN_WIDTH//2, SCREEN_HEIGHT//2)).center)
        screen.blit(rotatedImage, renderRect)

    def shootBullet(self):
        """Generates a new bullet originating from the player

        Returns:
            src.ships.bullet.newBullet: The bullet that was created to be added to the bullets list
        """
        bulletPos = self.position[:]
        bulletSpeed = self.speed+30
        bulletAngle = self.angle+0
        bullet = src.ships.bullet.newBullet(bulletPos, bulletSpeed, bulletAngle, "player")

        print(bullet.speed)
        return bullet
