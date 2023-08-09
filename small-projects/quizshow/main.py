import sys
import os
import time

import math
import textstrs
from textstrs import *
from gen_colors import gen_colors
import game
# initialise everything and check stuff
global curses
global screen
global term_height
global term_width


def add_str_center(in_str, centerx=-1, y = 0, color = 0):
    '''a func that adds a string to the screen centered at a given location'''

    if centerx == -1:
        screen.addstr(y, term_width//2 - len(in_str)//2, in_str,
                      curses.color_pair(color))




try:
    import curses
except ModuleNotFoundError:
    print("""
    Error: curses could not be imported error: ModuleNotFoundError this is 
    likley because the windows-curses package is not installed (while curses 
    is a preinstalled python module, it doesn't work on windows by default)
    To fix this install the windows-curses package with 
    'pip install windows-curses' or 'py -m pip install windows-curses'
    """)
    sys.exit(1)


if "idlelib" in sys.modules:
    print("This program does not work in idle shell. Please run it from"
          "terminal")

try:
    screen = curses.initscr()
except ModuleNotFoundError:
    print("error, could not create screen. This is most likely because you are"
          "running from an IDE shell and not a terminal. Please run this"
          "program from a terminal")
    sys.exit(1)

print(textstrs.controlstext)
term_height = os.get_terminal_size().lines
term_width = os.get_terminal_size().columns
curses.start_color()
gen_colors(curses)

curses.curs_set(False)
screen.keypad(True)
curses.noecho()

curses.init_pair(1, 1, 0)
curses.init_pair(2, 0, 1)

# Welcome screen
for count, i in enumerate(textstrs.welcometext.split("\n")):
    add_str_center(i, -1, round(term_height/2)-4+count, 1)

add_str_center("[Press any key to start]", -1, round(term_height/2)+1, 2)
screen.refresh()
screen.getch()
screen.clear()
#     screen.addstr(round((term_height/2)-4)+count, round(term_width/2-int(len(i)/2)), i)


# Controls screen
for count, i in enumerate(textstrs.controlstext.split("\n")):
    add_str_center(i, -1, round(term_height/2)-4+count, 1)

add_str_center("[start]", -1, term_height//2 + 4, 2)

# for checking when enter is pressed on controls screen

while True:
    char = screen.getch()
    if char == 10:
        break
    screen.addstr(0, 0, str(char)+"          ")
    screen.refresh()

screen.clear()

for count, i in enumerate(textstrs.quizshowtext.split("\n")):
    add_str_center(i, -1, round(term_height/2)-12+count, 1)
    

add_str_center(quizoptions[0], -1, (term_height//2)-6, 2)
add_str_center(quizoptions[1], -1, (term_height//2)-4, 1)
add_str_center(quizoptions[2], -1, (term_height//2)-2, 1)
add_str_center(quizoptions[3], -1, (term_height//2), 1)

sel = 0
while True:
    char = screen.getch()
    if char == 258 and sel != 3:  # down arrow
        # replace existing with blank
        add_str_center(quizoptions[sel], -1, (term_height//2)-6+(2*sel), 1) 
        sel += 1
        # make new selection highlighted
        add_str_center(quizoptions[sel], -1, (term_height//2)-6+(2*sel), 2)

    elif char == 259 and sel != 0:  # up arrow
        add_str_center(quizoptions[sel], -1, (term_height//2)-6+(2*sel), 1)
        sel -= 1
        # make new selection highlighted
        add_str_center(quizoptions[sel], -1, (term_height//2)-6+(2*sel), 2)
    elif char == 10:
        break



gameloop = True
if sel == 0:
    game.play_game(curses, screen)

while gameloop:
    screen.addstr(5, 5, f"term height: {term_height}")
    screen.addstr(6, 5, f"term width : {term_width}")
    screen.refresh()
    time.sleep(5)
