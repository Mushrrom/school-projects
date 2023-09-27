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
curses.curs_set(False)  # hide cursor
screen.keypad(True)  # use keypad (needed for arrow keys)
curses.noecho()  # don't print keys pressed to screen

# set up default colour palette (colour pair will be fg colour bg colour based on
# terminal colour palette)
# E.g 18 is black text with a white bg because colour code 1 for foreground is 
# black and colour code 8 for background is white
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

# add_str_center is defined in gamePrints.py to print strings at the center of
# the screen (basically copied straight from quiz show). It takes the string to
# add and Y position as inputs, along with an optional input for the colour
add_str_center("----------------------", 10)
add_str_center("|text based adventure|", 11)
add_str_center("----------------------", 12)

add_str_center("[        Play game        ]", 15, 18)
add_str_center("[ Continue from last save ]", 18)
print_borders()
sel = 0

# This is logic for selecting items. this code, or similar code is repeated
# a lot throughout my code, and not every time is fully commented. If you are 
# curious about the character codes. The "last key" thing in info shows the 
# character code (which is very useful for me to make the game)
while True:
    btn = screen.getch()  # screen.getch gets keyboard input as char code
    match btn:
        case 258:  # character code 258 is a down arrow
            if sel != 1:
                sel = 1
                add_str_center("[        Play game        ]", 15)
                add_str_center("[ Continue from last save ]", 18, 18)
        case 259:  # Character code 259 is up arrow
            if sel != 0:
                sel = 0
                add_str_center("[        Play game        ]", 15, 18)
                add_str_center("[ Continue from last save ]", 18)
        case 10:  # Character code 10 is enter
            break

# Keep track of how many game ticks have passed
tick = 0

# the location of the room
currentX = 0
currentY = 0

# if player does not want to continue save then delete all files in save folder
if sel == 0:
    filelist = os.listdir("saves/1")
    for f in filelist:
        os.remove(os.path.join("saves/1", f))

screen.clear()
print_borders()
# add whole story and stuff later
add_str_center("This is some story wow", 8)
add_str_center("Press the any key to continue", 14)
screen.getch()
player = newPlayer()
# addGameInfo(player)

screen.clear()

# player selects initial weapon
add_str_center("Choose your weapon (press enter to select)", 5)
add_str_center("stormbreaker blade - dmg: 10, modifier: 35", 10, 18)
add_str_center("Bloodmoon Dagger - dmg: 20, modifier: 10", 12)
add_str_center("Stick - dmg: 1, modifier: 1", 14)
sel = 0
while True:
    # Selection logic
    match screen.getch():
        case 258:
            if sel != 2:
                sel += 1
        case 259:
            if sel != 0:
                sel -= 1
        case 10:
            break

    # Highlight current selection (absolutley horrible code)
    if sel == 0:  # thanks for the names chatgpt
        add_str_center("stormbreaker blade - dmg: 10, modifier: 35", 10, 18)
        add_str_center("Bloodmoon Dagger - dmg: 20, modifier: 10", 12)
        add_str_center("Stick - dmg: 1, modifier: 1", 14)
    elif sel == 1:
        add_str_center("stormbreaker blade - dmg: 10, modifier: 35", 10)
        add_str_center("Bloodmoon Dagger - dmg: 20, modifier: 10", 12, 18)
        add_str_center("Stick - dmg: 1, modifier: 1", 14)
    else:
        add_str_center("stormbreaker blade - dmg: 10, modifier: 35", 10)
        add_str_center("Bloodmoon Dagger - dmg: 20, modifier: 10", 12)
        add_str_center("Stick - dmg: 1, modifier: 1", 14, 18)

# set weapon based on player selection
if sel == 0:
    player.pickupItem("stormbreaker blade")
    player.setWeapon("stormbreaker blade")
elif sel == 1:
    player.pickupItem("Bloodmoon Dagger")
    player.setWeapon("Bloodmoon Dagger")
else:
    player.pickupItem("stick")
    player.setWeapon("stick")

screen.clear()
level = createLevel(0, 0, 1)
level.renderLevel()

# test items
player.pickupItem("test", 40)
player.pickupItem("test", 3)
player.pickupItem("test2", 1)
player.pickupItem("test2", 2)
player.pickupItem("stick")

while True:
    key = screen.getch()

    # This handles player movement, it first checks what direction the
    # player is moving, then checks whether they are going to go into a
    # wall. And then the elif checks if the wall is actually an exit that
    # the player can go into. The numbers are because when curses gets a
    # keyboard input it stores it as a character code
    match key:
        case 258:  # move down
            if not level.player_pos[1] >= 26:
                level.movePlayer([0, 1], player)
            elif level.exits[3] == 1 and 51 < level.player_pos[0] < 57:
                level.movePlayer([0, 1], player)
        case 259:  # move up
            if not level.player_pos[1] <= 6:
                level.movePlayer([0, -1], player)
            elif level.exits[2] == 1 and 51 < level.player_pos[0] < 57:
                level.movePlayer([0, -1], player)
        case 261:  # Move right
            if not level.player_pos[0] >= 102:
                level.movePlayer([1, 0], player)
            elif level.exits[0] == 1 and 12 < level.player_pos[1] < 18:
                level.movePlayer([1, 0], player)
        case 260:  # Move left
            if not level.player_pos[0] <= 6:
                level.movePlayer([-1, 0], player)
            elif level.exits[1] == 1 and 12 < level.player_pos[1] < 18:
                level.movePlayer([-1, 0], player)
        case 105:
            player.showInventory()

    tick += 1

    # checks if the player should be moving to a different room, and moves
    # them to a different room if they are. See createLevel.py for more
    # info on what this function does
    if level.player_pos[1] == 0:
        currentY += 1
        level = createLevel(currentX, currentY, 0)
    if level.player_pos[1] == 32:
        currentY -= 1
        level = createLevel(currentX, currentY, 1)
    if level.player_pos[0] == 0:
        currentX += 1
        level = createLevel(currentX, currentY, 2)
    if level.player_pos[0] == 108:
        currentX -= 1
        level = createLevel(currentX, currentY, 3)

    # Update enemies and render level + game info
    level.updateEnemies()
    level.renderLevel()
    addGameInfo(player, key, tick, currentX, currentY)

screen.getch()

