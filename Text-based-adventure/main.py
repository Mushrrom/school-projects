import sys
import os

from consts import * 
from gamePrints import *
from createGame import newPlayer
from createLevel import createLevel


# game screen size will be 35x110
screen_y, screen_x = screen.getmaxyx()
if screen_y < 35 or screen_x < 110:
    print("screen must be at least 110x35")
    sys.exit(1)
curses.resize_term(35, 110) # resize the screen to 35x110

# Create save location
if not os.path.exists("saves/1/"):
    os.mkdir("saves/1/")

# Curses config
curses.curs_set(False)
screen.keypad(True)
curses.noecho()

# set up default colour palette (colour pair will be fg colour bg colour based on
# terminal colour palette)
# This sets it up with the first number being FG and the second being BG
curses.start_color()
curses.use_default_colors()
for i in range(9):
    for j in range(9):
        i_str = str(i+1)
        j_str = str(j+1)
        curses.init_pair(int(i_str+j_str), i, j)

# for testing colours
for i in range(1, 9):
    for j in range(1, 9):
        screen.addstr(i, j*3, str(i)+str(j), curses.color_pair(int(str(i)+str(j))))

# add_str_cetner is defined in gamePrints.py to print strings at the center of
# the screen (basically copied straight from quiz show)
add_str_center("----------------------", 10)
add_str_center("|text based adventure|", 11)
add_str_center("----------------------", 12)

add_str_center("[ Play game ]", 15, 18)
add_str_center("[ Open save ]", 18)
print_borders()
sel = 0
while True:
    btn = screen.getch()  # screen.getch gets keyboard input as char code
    match btn:
        case 258:  # character code 258 is a down arrow
            if sel != 1:
                sel = 1
                add_str_center("[ Play game ]", 15)
                add_str_center("[ Open save ]", 18, 18)
        case 259:  # Character code 259 is up arrow
            if sel != 0:
                sel = 0
                add_str_center("[ Play game ]", 15, 18)
                add_str_center("[ Open save ]", 18)
        case 10:  # Character code 10 is enter
            break

# Keep track of how many game ticks have passed
tick = 0
if sel == 0:
    screen.clear()
    print_borders()
    # add whole story and stuff later
    add_str_center("This is some story wow", 8)
    add_str_center("Press the any key to continue", 14)

    player = newPlayer()
    # addGameInfo(player)

    level = createLevel(0, 0, 1)
    level.renderLevel()
    while True:
        key = screen.getch()
        tick += 1
        level.movePlayer([0, 1], player)
        level.updateEnemies()
        level.renderLevel()
        addGameInfo(player, key, tick)

screen.getch()

