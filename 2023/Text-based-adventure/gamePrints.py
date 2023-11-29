'''A collection of things to be printed by the game that will need to be printed
 a lot'''

from consts import *

def add_str_center(printString, string_y, colour = 2):
    '''Add a string at the center of the screen (input string to print and y
    location of the string)'''
    string_length = len(printString)
    string_x = 54 - string_length//2
    screen.addstr(string_y, string_x, printString, curses.color_pair(colour))



def print_borders():
    '''print the borders of the screen''' 
    for i in range(108): #  Top border
        screen.addch(0, i, "-")
    for i in range(108): #  Bottom border
        screen.addch(34, i, "-")
    for i in range(108): #  Border between game and game info
        screen.addch(32, i, "-")

    for i in range(35):  # left vertical border
        screen.addch(i, 0, '|')
    for i in range(35):  # right vertical border
        screen.addch(i, 108, '|')


def addGameInfo(player, key, tick, x, y):
    '''add game info to bottom of screen'''
    screen.addstr(33, 1, f"health: {player.health}")
    screen.addstr(33, 15, f"score: {player.score}")
    screen.addstr(33, 30, f"tick: {tick}")
    screen.addstr(33, 45, f"last key: {key}")

    for i in range(1, 9):
        screen.addstr(33, 98+i, str(i), curses.color_pair(i+10))

    screen.addstr(33, 60, f"x: {x}")
    screen.addstr(33, 65, f"y: {y}")


def waitUntilEnter():
    '''Waits until enter key is pressed'''
    while True:
        if screen.getch() == 10:
            break
