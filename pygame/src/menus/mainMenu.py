import pygame
import pygame_gui
import pygame.freetype
from pygame.locals import *

from src.consts import *

def renderMenu(screen: pygame.surface):
    """Makes the main menu

    Args:
        screen (pygame.surface): screen to render the menu to

    Returns:
        int: What to do after the menu
    """
    clock = pygame.time.Clock()

    arrows = pygame.image.load("assets/arrows.png")
    c_key = pygame.image.load("assets/c_key.png")
    sel = 0 # current selection
    menuLoop = True
    while menuLoop:
        # Handle inputs
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == KEYDOWN:
                if event.key == K_UP and sel > 0:
                    sel -= 1
                elif event.key == K_DOWN and sel < 2:
                    sel += 1
                elif event.key == K_c:
                    return sel

        # Render options
        screen.fill(BG)
        GAME_FONT.render_to(screen, (270, 100), "Spacewar! 2", (255, 255, 255))
        GAME_FONT.render_to(screen, (270, 200), "  Play game  ", (255, 255, 255))
        GAME_FONT.render_to(screen, (234, 260), "   View high scores   ", (255, 255, 255))
        GAME_FONT.render_to(screen, (310, 320), "  Quit  ", (255, 255, 255))

        # Render option > selections <
        if sel == 0:
            GAME_FONT.render_to(screen, (215, 200),
                                ">                                               <", (255, 255, 255))
        elif sel == 1:
            GAME_FONT.render_to(screen, (215, 260),
                                ">                                               <", (255, 255, 255))
        elif sel == 2:
            GAME_FONT.render_to(screen, (215, 320),
                                ">                                               <", (255, 255, 255))

        # Instructions for how to use the menu
        GAME_FONT.render_to(screen, (10, 450), "Select :", (255, 255, 255))
        screen.blit(arrows, (103, 445))

        GAME_FONT.render_to(screen, (150, 450), "Confirm :", (255, 255, 255))
        screen.blit(c_key, (261, 452))


        pygame.display.update()
        clock.tick(60)

    return sel
