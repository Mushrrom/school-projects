import os
import json

import pygame
from pygame.locals import *

from src.consts import *

chars = list("-ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890")

def saveHighScore(screen: any, score: int, clock: any):
    """Save high scores

    Args:
        screen (any): Pygame screen to render to
        score (int): The score
        clock (any): Pygame clock
    """
    # Arrow assets
    arrow_down_empty = pygame.image.load("assets/arrow_down_empty.png")
    arrow_up_empty = pygame.image.load("assets/arrow_up_empty.png")
    arrow_down_filled = pygame.image.load("assets/arrow_down_filled.png")
    arrow_up_filled = pygame.image.load("assets/arrow_up_filled.png")

    c_key = pygame.image.load("assets/c_key.png")

    # Make scores file if it doesn't already exist
    if not os.path.exists("scores.json"):
        with open("scores.json", "w") as f:
            json.dump({
                "highScores" : [
                    {"name": "------", "score": 0},
                    {"name": "------", "score": 0},
                    {"name": "------", "score": 0},
                    {"name": "------", "score": 0},
                    {"name": "------", "score": 0},
                ]
            }, f)

    with open("scores.json", "r") as f:
        scores = json.load(f)

    if scores["highScores"][4]["score"] < score:
        screen.fill(BG)

        # Say u got high score
        GAME_FONT.render_to(screen, (210, 230), "You got a high score!", (255, 255, 255))
        GAME_FONT.render_to(screen, (250, 300), "Continue :", (255, 255, 255))
        screen.blit(c_key, (381, 302))

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

        # Get the player's name
        loop = True
        nameList = [0, 0, 0, 0, 0, 0]
        sel = 0
        while loop:
            screen.fill(BG)
            # Input to select character
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == KEYDOWN:
                    if event.key == K_UP:
                        if nameList[sel] == 36:
                            nameList[sel] = 0
                        else:
                            nameList[sel] += 1

                    elif event.key == K_DOWN:
                        if nameList[sel] == 0:
                            nameList[sel] = 36
                        else:
                            nameList[sel] -= 1

                    elif event.key == K_LEFT:
                        if sel == 0:
                            sel = 5
                        else:
                            sel -= 1

                    elif event.key == K_RIGHT:
                        if sel == 5:
                            sel = 0
                        else:
                            sel += 1

                    elif event.key == K_c:
                        loop = False

            GAME_FONT.render_to(screen, (230, 200), "Enter your name", (255, 255, 255))

            # Make the actual selection menu - makes filled arrows if its selected otherwise makes
            # empty
            for count, i in enumerate(nameList):
                if count == sel:
                    screen.blit(arrow_down_filled, (268+20*count, 320))
                    screen.blit(arrow_up_filled, (268+20*count, 287))
                else:
                    screen.blit(arrow_down_empty, (268+20*count, 320))
                    screen.blit(arrow_up_empty, (268+20*count, 287))
                GAME_FONT.render_to(screen, (270+20*count, 300), chars[i], (255, 255, 255))

            GAME_FONT.render_to(screen, (150, 450), "Confirm :", (255, 255, 255))
            screen .blit(c_key, (261, 452))
            pygame.display.update()
            clock.tick(60)

        # Format player's name
        name = ""
        for i in nameList:
            name += chars[i]
        name = name.strip("-")
        if len(name) == 0: name = "-"

        # Remove bottom score and add players score
        scores["highScores"].pop(4)
        scores["highScores"].append({"name": name, "score": score})

        # Sorts high scores by score (high to low)
        scores['highScores'] = sorted(scores['highScores'], key=lambda x : x['score'], reverse=True)

        # Save high score
        with open("scores.json", "w") as f:
            json.dump(scores, f)



