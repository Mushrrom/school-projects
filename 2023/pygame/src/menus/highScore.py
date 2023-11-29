import json
import os

import pygame
from pygame.locals import *

from src.consts import *
def showHighScores(screen):
    clock = pygame.time.Clock()
    if not os.path.exists("scores.json"): # Dont show menu if no high scores
        return

    with open("scores.json", "r") as f:
        scores = json.loads(f.read())

    screen.fill(BG)

    # Title
    GAME_FONT.render_to(screen, (250, 100), "High scores: ", (255, 255, 255))

    # Add all the scores and names
    for count, i in enumerate(scores["highScores"]):
        GAME_FONT.render_to(screen, (270, 170+30*count), f"{i['name']} : {i['score']}", (255, 255, 255))

    pygame.display.update()

    # Wait until c key pressed
    loop = True
    while loop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == KEYDOWN:
                if event.key == K_c:
                    loop = False

        clock.tick(60)

    return