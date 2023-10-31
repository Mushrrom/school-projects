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
        rect (pygame.Rect): The players rect (Used for).
        collideRect (pygame.rect): A smaller rect used for collisions.
        health (int): The health of the player.
    """
    def __init__(self):
        # Constant amount for speed
        self.speed = 0.1

        # player values for amount to move
        self.rotationAmount = 0
        self.velocity = [0, 0]

        # player values for current position+angle
        self.position = [250, 250]
        self.angle = 0

        # image + rect
        self.img = pygame.transform.scale_by(pygame.image.load("assets/test_image.png"), 3)
        self.rect = self.img.get_rect()

        self.collideRect = pygame.transform.scale_by(self.img, 0.5).get_rect()
        self.collideRect.center = self.rect.center

        # Health amount
        self.health = 0

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
            # For actually moving the player, this uses the angle of the player and then calculates
            # what to add to the x and y velocity based on that. Its just trigonometry
            self.velocity[0] += -1*math.sin(self.angle*math.pi/180)*self.speed
            self.velocity[1] += -1*math.cos(self.angle*math.pi/180)*self.speed

    def move(self):
        """Moves the player based on their x and y velocities
        """
        # add to current position based on velocity
        self.position[0] += self.velocity[0]
        self.position[1] += self.velocity[1]


    def render(self, screen: pygame.display):
        """Renders the player to the center of the screen

        Args:
            screen (pygame.display): Game screen
        """
        # Rotate player image
        rotatedImage = pygame.transform.rotate(self.img, self.angle)

        # Rect of self for colission calculations
        self.rect = rotatedImage.get_rect(center = self.img.get_rect(center = (self.position[0], self.position[1])).center)
        self.collideRect.center = self.rect.center

        # Rect that will render to center of screen for what the person sees
        renderRect = rotatedImage.get_rect(center = self.img.get_rect(center = (SCREEN_WIDTH//2, SCREEN_HEIGHT//2)).center)
        screen.blit(rotatedImage, renderRect)

    def shootBullet(self):
        """Generates a new bullet originating from the player

        Returns:
            src.ships.bullet.newBullet: The bullet that was created to be added to the bullets list
        """
        bulletPos = self.position[:]
        bulletSpeed = 30
        bulletAngle = self.angle+0
        bullet = src.ships.bullet.newBullet(bulletPos, bulletSpeed, bulletAngle, "player")

        print(bullet.speed)
        return bullet
