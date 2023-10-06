import pygame
import pygame_gui
import pygame.freetype

from src.consts import *
def renderMenu(screen):
    pygame.freetype.init()
    guiManager =  pygame_gui.UIManager((800, 600))

    playGameButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((220, 215), (200, 50)),
                                                text='Play game!',
                                                manager=guiManager)
    viewHighScoreButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((220, 300), (200, 50)),
                                                text='View high scores',
                                                manager=guiManager)

    clock = pygame.time.Clock()
    menuLoop = True

    while menuLoop:
        timeDelta = clock.tick(60)/1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menuLoop = False
                pygame.quit()
                return "quit"

            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == playGameButton:
                    menuLoop = False
                    return "playGame"
                elif event.ui_element == viewHighScoreButton:
                    menuLoop = False
                    return "viewHighScores"


            guiManager.process_events(event)

        screen.fill(BG)

        guiManager.update(timeDelta)
        guiManager.draw_ui(screen)

        pygame.display.update()
