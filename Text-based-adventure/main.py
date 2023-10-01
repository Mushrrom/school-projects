import sys
import os
import random
import time

from consts import * 
from gamePrints import *
from createPlayer import newPlayer
from createLevel import createLevel


# game screen size will be 35x110
# screen_y, screen_x = screen.getmaxyx()
# if screen_y < 35 or screen_x < 110:
#     print("screen must be at least 110x35")
#     sys.exit(1)


curses.resize_term(35, 110) # resize the terminal to 35x110

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

# if player does not want to continue save then delete all files in save folder
if sel == 0:
    filelist = os.listdir("saves/1")
    for f in filelist:
        os.remove(os.path.join("saves/1", f))

startTime = time.time()
screen.clear()
print_borders()

# First bit of story
screen.addstr(4, 10, "Hello adventurer")

screen.addstr(6, 10, "A demon has destroyed your home. In order to save it")
screen.addstr(7, 10, "you must venture deep into the underworld and defeat")
screen.addstr(8, 10, "it.")

screen.addstr(10, 10, "Other adventurers have attempted to defeat the demon,")
screen.addstr(11, 10, "and they have all failed. We believe the demon has been")
screen.addstr(12, 10, "able to reincarnate the failed adventurers to fight you")

screen.addstr(14, 10, "Good luck adventurer,")
screen.addstr(15, 10, "A▓r▒▓ ▒a▓▒e░ ░r▓y")

add_str_center("[ continue ]", 20, 18)
waitUntilEnter()
screen.clear()

# Variables for the game
# -----------------------------

# Keep track of how many game ticks have passed
tick = 0

# the location of the room
currentX = 0
currentY = 0

# Current level
level = 1

# Player (Stores inventory, health, etc. newPlayer is in createPlayer.py)
player = newPlayer()

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

# Get timstamp at start of game (for calculating time taken)
initialTime = time.time()


screen.clear()
level = createLevel(0, 0, 1, True, [1, 1, 1, 1])
level.renderLevel(player)
levelNum = 1

exploredRooms = 0
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
                level.movePlayer([0, 1], player, levelNum)
            elif level.exits[3] == 1 and 51 < level.player_pos[0] < 57:
                level.movePlayer([0, 1], player, levelNum)
        case 259:  # move up
            if not level.player_pos[1] <= 6:
                level.movePlayer([0, -1], player, levelNum)
            elif level.exits[2] == 1 and 51 < level.player_pos[0] < 57:
                level.movePlayer([0, -1], player, levelNum)
        case 261:  # Move right
            if not level.player_pos[0] >= 102:
                level.movePlayer([1, 0], player, levelNum)
            elif level.exits[0] == 1 and 12 < level.player_pos[1] < 18:
           time.time()     level.movePlayer([1, 0], player, levelNum)
        case 260:  # Move left
            if not level.player_pos[0] <= 6:
                level.movePlayer([-1, 0], player, levelNum)
            elif level.exits[1] == 1 and 12 < level.player_pos[1] < 18:
                level.movePlayer([-1, 0], player, levelNum)
        case 105: # key "i" - shows inventory
            player.showInventory()

    tick += 1

    # checks if the player should be moving to a different room, and moves
    # them to a different room if they are. See createLevel.py for more
    # info on what this function does
    if level.player_pos[1] == 0:
        currentY += 1
        level = createLevel(currentX, currentY, 0)
        exploredRooms += 1
    if level.player_pos[1] == 32:
        currentY -= 1
        level = createLevel(currentX, currentY, 1)
        exploredRooms += 1
    if level.player_pos[0] == 0:
        currentX += 1
        level = createLevel(currentX, currentY, 2)
        exploredRooms += 1
    if level.player_pos[0] == 108:
        currentX -= 1
        level = createLevel(currentX, currentY, 3)
        exploredRooms += 1

    # Update enemies and render level + game info
    level.updateEnemies()
    level.renderLevel(player)
    addGameInfo(player, key, tick, currentX, currentY)

    # Escape the game loop after 10 rooms explored to go to boss fight
    if exploredRooms == 2:
        break

# ------------------------------------------
# Boss fight 1:
# ------------------------------------------

# story 
screen.clear()
add_str_center("You walk into the room and all of the exits close around you", 3)
add_str_center("[ contunue ]", 5, 18)
waitUntilEnter()
level = createLevel(99, 99, 2, True, [0, 0, 0, 0], [50, 25])
level.enemies = [[60, 8]]
level.enemies_health = [200]


levelNum = 1

bossTick = 0
while True:
    key = screen.getch()

    killedBoss = False
    match key:
        case 258:  # move down
            if not level.player_pos[1] >= 26:
                killedBoss = level.movePlayerBoss([0, 1], player, levelNum)
            elif level.exits[3] == 1 and 51 < level.player_pos[0] < 57:
                killedBoss = level.movePlayerBoss([0, 1], player, levelNum)
        case 259:  # move up
            if not level.player_pos[1] <= 6:
                killedBoss = level.movePlayerBoss([0, -1], player, levelNum)
            elif level.exits[2] == 1 and 51 < level.player_pos[0] < 57:
                killedBoss = level.movePlayerBoss([0, -1], player, levelNum)
        case 261:  # Move right
            if not level.player_pos[0] >= 102:
                killedBoss = level.movePlayerBoss([1, 0], player, levelNum)
            elif level.exits[0] == 1 and 12 < level.player_pos[1] < 18:
                killedBoss = level.movePlayerBoss([1, 0], player, levelNum)
        case 260:  # Move left
            if not level.player_pos[0] <= 6:
                killedBoss = level.movePlayerBoss([-1, 0], player, levelNum)
            elif level.exits[1] == 1 and 12 < level.player_pos[1] < 18:
                killedBoss = level.movePlayerBoss([-1, 0], player, levelNum)
        case 105: # key "i" - shows inventory
            player.showInventory()

    if killedBoss:
        break
    level.updateEnemies(True, ["down"])
    level.renderLevel(player, True)
    addGameInfo(player, key, tick, currentX, currentY)

    if bossTick % 10 == 0:
        for i in range(96):
            if random.randint(0, 5) != 3:
                level.enemies.append([6+i, 6])
                level.enemies_health.append(0)

    bossTick += 1
    tick += 1

screen.clear()

add_str_center("You defeated the adventurer and you see two items that the", 15)
add_str_center("adventurer was wearing lying on the ground", 16)
add_str_center("[ continue ]", 18, 18)
waitUntilEnter()
screen.clear()

add_str_center("Choose which to pick up", 12)
add_str_center("Adventurer's dagger", 15, 18)
add_str_center("Adventurer's chestplate", 18)
while True:
    btn = screen.getch()  # screen.getch gets keyboard input as char code
    match btn:
        case 258:  # character code 258 is a down arrow
            if sel != 1:
                sel = 1
                add_str_center("Adventurer's dagger", 15)
                add_str_center("Adventurer's chestplate", 18, 18)
        case 259:  # Character code 259 is up arrow
            if sel != 0:
                sel = 0
                add_str_center("Adventurer's dagger", 15, 18)
                add_str_center("Adventurer's chestplate", 18)
        case 10:  # Character code 10 is enter
            break

screen.clear()
if sel == 0:
    add_str_center("You pick up the Adventurer's dagger right before the", 15)
    add_str_center("Floor falls out beneath you, Sending you to the next level", 16)
    add_str_center("[ continue ]", 18, 18)
    player.pickupItem("adventurer's dagger")
    waitUntilEnter()
else:
    add_str_center("You go to pick up the adventurer's chestplate, but as you", 15)
    add_str_center("Try to pick it up it falls apart in your hands. As you are", 16)
    add_str_center("trying to pick up any remaining pieces off the ground, ", 17)
    add_str_center("the ground falls out underneath you. Sending you to the", 18)
    add_str_center("next level", 19)
    add_str_center("[ contunue ]", 21, 18)
    waitUntilEnter()

player.score += 2000
# ----------------------------
# Level 2 
# ----------------------------

screen.clear()
level = createLevel(0, 0, 1, True, [1, 1, 1, 1])
level.renderLevel(player)

currentX = 0
currentY = 0
exploredRooms = 0

levelNum = 2

# basically just copied from above
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
                level.movePlayer([0, 1], player, levelNum)
            elif level.exits[3] == 1 and 51 < level.player_pos[0] < 57:
                level.movePlayer([0, 1], player, levelNum)
        case 259:  # move up
            if not level.player_pos[1] <= 6:
                level.movePlayer([0, -1], player, levelNum)
            elif level.exits[2] == 1 and 51 < level.player_pos[0] < 57:
                level.movePlayer([0, -1], player, levelNum)
        case 261:  # Move right
            if not level.player_pos[0] >= 102:
                level.movePlayer([1, 0], player, levelNum)
            elif level.exits[0] == 1 and 12 < level.player_pos[1] < 18:
                level.movePlayer([1, 0], player, levelNum)
        case 260:  # Move left
            if not level.player_pos[0] <= 6:
                level.movePlayer([-1, 0], player, levelNum)
            elif level.exits[1] == 1 and 12 < level.player_pos[1] < 18:
                level.movePlayer([-1, 0], player, levelNum)
        case 105: # key "i" - shows inventory
            player.showInventory()

    tick += 1

    # checks if the player should be moving to a different room, and moves
    # them to a different room if they are. See createLevel.py for more
    # info on what this function does
    if level.player_pos[1] == 0:
        currentY += 1
        level = createLevel(currentX, currentY, 0)
        exploredRooms += 1
    if level.player_pos[1] == 32:
        currentY -= 1
        level = createLevel(currentX, currentY, 1)
        exploredRooms += 1
    if level.player_pos[0] == 0:
        currentX += 1
        level = createLevel(currentX, currentY, 2)
        exploredRooms += 1
    if level.player_pos[0] == 108:
        currentX -= 1
        level = createLevel(currentX, currentY, 3)
        exploredRooms += 1

    # Update enemies and render level + game info
    level.updateEnemies()
    level.renderLevel(player)
    addGameInfo(player, key, tick, currentX, currentY)

    # Escape the game loop after 10 rooms explored to go to boss fight
    if exploredRooms == 10:
        break


# ----------------------
# Boss fight 2 
# ----------------------
screen.clear()
add_str_center("You walk into the room and all of the exits close around you", 3)
add_str_center("[ contunue ]", 5, 18)
waitUntilEnter()
level = createLevel(99, 99, 2, True, [0, 0, 0, 0], [50, 25])
level.enemies = [[60, 8]]
level.enemies_health = [400]

bossTick = 0
while True:
    key = screen.getch()

    killedBoss = False
    match key:
        case 258:  # move down
            if not level.player_pos[1] >= 26:
                killedBoss = level.movePlayerBoss([0, 1], player, levelNum)
            elif level.exits[3] == 1 and 51 < level.player_pos[0] < 57:
                killedBoss = level.movePlayerBoss([0, 1], player, level)
        case 259:  # move up
            if not level.player_pos[1] <= 6:
                killedBoss = level.movePlayerBoss([0, -1], player, levelNum)
            elif level.exits[2] == 1 and 51 < level.player_pos[0] < 57:
                killedBoss = level.movePlayerBoss([0, -1], player, levelNum)
        case 261:  # Move right
            if not level.player_pos[0] >= 102:
                killedBoss = level.movePlayerBoss([1, 0], player, levelNum)
            elif level.exits[0] == 1 and 12 < level.player_pos[1] < 18:
                killedBoss = level.movePlayerBoss([1, 0], player, levelNum)
        case 260:  # Move left
            if not level.player_pos[0] <= 6:
                killedBoss = level.movePlayerBoss([-1, 0], player, levelNum)
            elif level.exits[1] == 1 and 12 < level.player_pos[1] < 18:
                killedBoss = level.movePlayerBoss([-1, 0], player, levelNum)
        case 105: # key "i" - shows inventory
            player.showInventory()

    if killedBoss:
        break
    level.updateEnemies(True, ["down"])
    level.renderLevel(player, True)
    addGameInfo(player, key, tick, currentX, currentY)

    if bossTick % 10 == 0:
        for i in range(96):
            if random.randint(0, 5) != 3:
                level.enemies.append([6+i, 6])
                level.enemies_health.append(0)

    bossTick += 1
    tick += 1
screen.clear()
add_str_center("You defeat the boss and go to the next level", 14)
add_str_center("[ continue ]", 16, 18)
waitUntilEnter()
# ----------------------
# Level 3
# ----------------------

levelNum = 3
screen.clear()
# person who asks for coins
add_str_center("You see a man sitting on the ground. You go up to him to see", 14)
add_str_center("what he is doing here", 15)
add_str_center("[ continue ]", 17, 18)
waitUntilEnter()
screen.clear()
add_str_center("He says: \"Kind adventurer, could I please have 20 coins?\"", 12)
add_str_center("Give 20 coins", 15, 18)
add_str_center("Don't give 20 coins", 18)

while True:
    btn = screen.getch()  # screen.getch gets keyboard input as char code
    match btn:
        case 258:  # character code 258 is a down arrow
            if sel != 1:
                sel = 1
                add_str_center("Give 20 coins", 15)
                add_str_center("Don't give 20 coins", 18, 18)
        case 259:  # Character code 259 is up arrow
            if sel != 0:
                sel = 0
                add_str_center("Give 20 coins", 15, 18)
                add_str_center("Don't give 20 coins", 18)
        case 10:  # Character code 10 is enter
            break

gaveCoins = False
screen.clear()
if sel == 0:
    if not "coin" in player.inventory[0]:
        add_str_center("You dont have any coins to give", 14)
        screen.getch()
    else:
        amountOfCoins = player.inventory[0][player.inventory[1].index("coin")]
        if amountOfCoins < 20:
            add_str_center("You dont have 20 coins to give :(", 14)
            screen.getch()
        else:
            player.removeItem("coin", 20)

            add_str_center('"Thank you adventurer"', 16)
            add_str_center("[ continue ]", 18, 18)
            waitUntilEnter()
            screen.clear()
            add_str_center("All of a sudden he vanishes and where he is sitting there", 15)
            add_str_center("is a path leading to the next level", 16)
            add_str_center("[ contunue ]", 18, 18)
            waitUntilEnter()
            gaveCoins = True
else:
    add_str_center("The man looks at you dissapointed", 16)
    add_str_center("[ continue ]", 18, 18)
    screen.clear()
    add_str_center("You decide to contunue your adventure", 16)
    add_str_center("[ continue ]", 18, 18)
    gaveCoins = False

screen.clear()
# rest of level 3:
if not gaveCoins: # if we did give coins then dont do level 3
    screen.clear()
    level = createLevel(0, 0, 1, True, [1, 1, 1, 1])
    level.renderLevel(player)

    currentX = 0
    currentY = 0
    exploredRooms = 0

    levelNum = 3

# basically just copied from above
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
                    level.movePlayer([0, 1], player, levelNum)
                elif level.exits[3] == 1 and 51 < level.player_pos[0] < 57:
                    level.movePlayer([0, 1], player, levelNum)
            case 259:  # move up
                if not level.player_pos[1] <= 6:
                    level.movePlayer([0, -1], player, levelNum)
                elif level.exits[2] == 1 and 51 < level.player_pos[0] < 57:
                    level.movePlayer([0, -1], player, levelNum)
            case 261:  # Move right
                if not level.player_pos[0] >= 102:
                    level.movePlayer([1, 0], player, levelNum)
                elif level.exits[0] == 1 and 12 < level.player_pos[1] < 18:
                    level.movePlayer([1, 0], player, levelNum)
            case 260:  # Move left
                if not level.player_pos[0] <= 6:
                    level.movePlayer([-1, 0], player, levelNum)
                elif level.exits[1] == 1 and 12 < level.player_pos[1] < 18:
                    level.movePlayer([-1, 0], player, levelNum)
            case 105: # key "i" - shows inventory
                player.showInventory()

        tick += 1

        # checks if the player should be moving to a different room, and moves
        # them to a different room if they are. See createLevel.py for more
        # info on what this function does
        if level.player_pos[1] == 0:
            currentY += 1
            level = createLevel(currentX, currentY, 0)
            exploredRooms += 1
        if level.player_pos[1] == 32:
            currentY -= 1
            level = createLevel(currentX, currentY, 1)
            exploredRooms += 1
        if level.player_pos[0] == 0:
            currentX += 1
            level = createLevel(currentX, currentY, 2)
            exploredRooms += 1
        if level.player_pos[0] == 108:
            currentX -= 1
            level = createLevel(currentX, currentY, 3)
            exploredRooms += 1

        # Update enemies and render level + game info
        level.updateEnemies()
        level.renderLevel(player)
        addGameInfo(player, key, tick, currentX, currentY)

        # Escape the game loop after 10 rooms explored to go to boss fight
        if exploredRooms == 10:
            break


# ----------------------
# Boss fight 3
# ----------------------
    screen.clear()
    add_str_center("You walk into the room and all of the exits close around you", 3)
    add_str_center("[ contunue ]", 5, 18)
    waitUntilEnter()
    level = createLevel(99, 99, 2, True, [0, 0, 0, 0], [50, 25])
    level.enemies = [[60, 8]]
    level.enemies_health = [400]

    bossTick = 0
    while True:
        key = screen.getch()

        killedBoss = False
        match key:
            case 258:  # move down
                if not level.player_pos[1] >= 26:
                    killedBoss = level.movePlayerBoss([0, 1], player, levelNum)
                elif level.exits[3] == 1 and 51 < level.player_pos[0] < 57:
                    killedBoss = level.movePlayerBoss([0, 1], player, level)
            case 259:  # move up
                if not level.player_pos[1] <= 6:
                    killedBoss = level.movePlayerBoss([0, -1], player, levelNum)
                elif level.exits[2] == 1 and 51 < level.player_pos[0] < 57:
                    killedBoss = level.movePlayerBoss([0, -1], player, levelNum)
            case 261:  # Move right
                if not level.player_pos[0] >= 102:
                    killedBoss = level.movePlayerBoss([1, 0], player, levelNum)
                elif level.exits[0] == 1 and 12 < level.player_pos[1] < 18:
                    killedBoss = level.movePlayerBoss([1, 0], player, levelNum)
            case 260:  # Move left
                if not level.player_pos[0] <= 6:
                    killedBoss = level.movePlayerBoss([-1, 0], player, levelNum)
                elif level.exits[1] == 1 and 12 < level.player_pos[1] < 18:
                    killedBoss = level.movePlayerBoss([-1, 0], player, levelNum)
            case 105: # key "i" - shows inventory
                player.showInventory()

        if killedBoss:
            break
        level.updateEnemies(True, ["down"])
        level.renderLevel(player, True)
        addGameInfo(player, key, tick, currentX, currentY)

        if bossTick % 10 == 0:
            for i in range(96):
                if random.randint(0, 5) != 3:
                    level.enemies.append([6+i, 6])
                    level.enemies_health.append(0)

        bossTick += 1
        tick += 1

    add_str_center("The ground falls out and you go to level 4. You can feel that", 15)
    add_str_center("You are close to the demon", 16)
    add_str_center("[ continue ]", 18, 18)



# ---------------------------
# Level 4 !!!!!!!
# ---------------------------

screen.clear()
level = createLevel(0, 0, 1, True, [1, 1, 1, 1])
level.renderLevel(player)

currentX = 0
currentY = 0
exploredRooms = 0

levelNum = 4

# basically just copied from above
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
                level.movePlayer([0, 1], player, levelNum)
            elif level.exits[3] == 1 and 51 < level.player_pos[0] < 57:
                level.movePlayer([0, 1], player, levelNum)
        case 259:  # move up
            if not level.player_pos[1] <= 6:
                level.movePlayer([0, -1], player, levelNum)
            elif level.exits[2] == 1 and 51 < level.player_pos[0] < 57:
                level.movePlayer([0, -1], player, levelNum)
        case 261:  # Move right
            if not level.player_pos[0] >= 102:
                level.movePlayer([1, 0], player, levelNum)
            elif level.exits[0] == 1 and 12 < level.player_pos[1] < 18:
                level.movePlayer([1, 0], player, levelNum)
        case 260:  # Move left
            if not level.player_pos[0] <= 6:
                level.movePlayer([-1, 0], player, levelNum)
            elif level.exits[1] == 1 and 12 < level.player_pos[1] < 18:
                level.movePlayer([-1, 0], player, levelNum)
        case 105: # key "i" - shows inventory
            player.showInventory()

    tick += 1

    # checks if the player should be moving to a different room, and moves
    # them to a different room if they are. See createLevel.py for more
    # info on what this function does
    if level.player_pos[1] == 0:
        currentY += 1
        level = createLevel(currentX, currentY, 0)
        exploredRooms += 1
    if level.player_pos[1] == 32:
        currentY -= 1
        level = createLevel(currentX, currentY, 1)
        exploredRooms += 1
    if level.player_pos[0] == 0:
        currentX += 1
        level = createLevel(currentX, currentY, 2)
        exploredRooms += 1
    if level.player_pos[0] == 108:
        currentX -= 1
        level = createLevel(currentX, currentY, 3)
        exploredRooms += 1

    # Update enemies and render level + game info
    level.updateEnemies()
    level.renderLevel(player)
    addGameInfo(player, key, tick, currentX, currentY)

    # Escape the game loop after 10 rooms explored to go to boss fight
    if exploredRooms == 10:
        break

add_str_center("There's another man sitting on the ground, right in front", 14)
add_str_center("of a door", 15)
add_str_center("[ continue ]", 17, 18)
waitUntilEnter()
screen.clear()
add_str_center('He says: "Give me 10 coins. Or else."', 12)
add_str_center("Give 10 coins", 15, 18)
add_str_center("Don't give 10 coins", 18)

while True:
    btn = screen.getch()  # screen.getch gets keyboard input as char code
    match btn:
        case 258:  # character code 258 is a down arrow
            if sel != 1:
                sel = 1
                add_str_center("Give 10 coins", 15)
                add_str_center("Don't give 10 coins", 18, 18)
        case 259:  # Character code 259 is up arrow
            if sel != 0:
                sel = 0
                add_str_center("Give 10 coins", 15, 18)
                add_str_center("Don't give 10 coins", 18)
        case 10:  # Character code 10 is enter
            break

gaveCoins = False
screen.clear()
if sel == 0:
    if not "coin" in player.inventory[0]:
        add_str_center("You dont have any coins to give", 14)
        screen.getch()
    else:
        amountOfCoins = player.inventory[0][player.inventory[1].index("coin")]
        if amountOfCoins < 20:
            add_str_center("You dont have 20 coins to give :(", 14)
            screen.getch()
        else:
            player.removeItem("coin", 20)

            add_str_center("He thanks you, and allows you to enter", 14)
            add_str_center("[ contunue ]", 16, 18)

            gaveCoins = True

if not gaveCoins:
    add_str_center("The man gets up and kills you. You die", 16)
    add_str_center("[ Continue ]", 18, 18)
    sys.exit()

# ----------------------
# Boss fight 4
# ----------------------
screen.clear()
add_str_center("You walk into the room and all of the exits close around you", 3)
add_str_center("[ contunue ]", 5, 18)
waitUntilEnter()
level = createLevel(99, 99, 2, True, [0, 0, 0, 0], [50, 25])
level.enemies = [[60, 8]]
level.enemies_health = [400]

bossTick = 0
while True:
    key = screen.getch()

    killedBoss = False
    match key:
        case 258:  # move down
            if not level.player_pos[1] >= 26:
                killedBoss = level.movePlayerBoss([0, 1], player, levelNum)
            elif level.exits[3] == 1 and 51 < level.player_pos[0] < 57:
                killedBoss = level.movePlayerBoss([0, 1], player, level)
        case 259:  # move up
            if not level.player_pos[1] <= 6:
                killedBoss = level.movePlayerBoss([0, -1], player, levelNum)
            elif level.exits[2] == 1 and 51 < level.player_pos[0] < 57:
                killedBoss = level.movePlayerBoss([0, -1], player, levelNum)
        case 261:  # Move right
            if not level.player_pos[0] >= 102:
                killedBoss = level.movePlayerBoss([1, 0], player, levelNum)
            elif level.exits[0] == 1 and 12 < level.player_pos[1] < 18:
                killedBoss = level.movePlayerBoss([1, 0], player, levelNum)
        case 260:  # Move left
            if not level.player_pos[0] <= 6:
                killedBoss = level.movePlayerBoss([-1, 0], player, levelNum)
            elif level.exits[1] == 1 and 12 < level.player_pos[1] < 18:
                killedBoss = level.movePlayerBoss([-1, 0], player, levelNum)
        case 105: # key "i" - shows inventory
            player.showInventory()

    if killedBoss:
        break
    level.updateEnemies(True, ["down"])
    level.renderLevel(player, True)
    addGameInfo(player, key, tick, currentX, currentY)

    if bossTick % 10 == 0:
        for i in range(96):
            if random.randint(0, 5) != 3:
                level.enemies.append([6+i, 6])
                level.enemies_health.append(0)

    bossTick += 1
    tick += 1


screen.clear()
add_str_center("The adventurer leaves some explosives on the ground. You pick", 14)
add_str_center("Them up. When you want to go the next room you can use them from", 15)
add_str_center("your inventory", 16)
add_str_center("[ continue ]", 18, 18)

player.pickupItem("explosives")
waitUntilEnter()

screen.clear()
add_str_center("You find yourself back in the room you started in on this level", 14)
add_str_center("[ continue ]", 16, 18)
waitUntilEnter()


# ----------------------
# Level 4 part 2 
# ----------------------

screen.clear()
level = createLevel(0, 0, 1, True, [1, 1, 1, 1])
level.renderLevel(player)

currentX = 0
currentY = 0
exploredRooms = 0

levelNum = 4

# basically just copied from above
while True:
    key = screen.getch()

    # This handles player movement, it first checks what direction the
    # player is moving, then checks whether they are going to go into a
    # wall. And then the elif checks if the wall is actually an exit that
    # the player can go into. The numbers are because when curses gets a
    # keyboard input it stores it as a character code
    usedExplosives = False
    match key:
        case 258:  # move down
            if not level.player_pos[1] >= 26:
                level.movePlayer([0, 1], player, levelNum)
            elif level.exits[3] == 1 and 51 < level.player_pos[0] < 57:
                level.movePlayer([0, 1], player, levelNum)
        case 259:  # move up
            if not level.player_pos[1] <= 6:
                level.movePlayer([0, -1], player, levelNum)
            elif level.exits[2] == 1 and 51 < level.player_pos[0] < 57:
                level.movePlayer([0, -1], player, levelNum)
        case 261:  # Move right
            if not level.player_pos[0] >= 102:
                level.movePlayer([1, 0], player, levelNum)
            elif level.exits[0] == 1 and 12 < level.player_pos[1] < 18:
                level.movePlayer([1, 0], player, levelNum)
        case 260:  # Move left
            if not level.player_pos[0] <= 6:
                level.movePlayer([-1, 0], player, levelNum)
            elif level.exits[1] == 1 and 12 < level.player_pos[1] < 18:
                level.movePlayer([-1, 0], player, levelNum)
        case 105: # key "i" - shows inventory
            usedExplosives = player.showInventory()

    tick += 1

    # checks if the player should be moving to a different room, and moves
    # them to a different room if they are. See createLevel.py for more
    # info on what this function does
    if level.player_pos[1] == 0:
        currentY += 1
        level = createLevel(currentX, currentY, 0)
        exploredRooms += 1
    if level.player_pos[1] == 32:
        currentY -= 1
        level = createLevel(currentX, currentY, 1)
        exploredRooms += 1
    if level.player_pos[0] == 0:
        currentX += 1
        level = createLevel(currentX, currentY, 2)
        exploredRooms += 1
    if level.player_pos[0] == 108:
        currentX -= 1
        level = createLevel(currentX, currentY, 3)
        exploredRooms += 1

    # Update enemies and render level + game info
    level.updateEnemies()
    level.renderLevel(player)
    addGameInfo(player, key, tick, currentX, currentY)

    # If used explosives then break to go to final battle
    if usedExplosives:
        break


# ----------------------
# final boss fight
# ----------------------

levelNum = 5
screen.clear()
add_str_center("You fall into a room and see the demon in front of you", 3)
add_str_center("[ contunue ]", 5, 18)
waitUntilEnter()
level = createLevel(99, 99, 2, True, [0, 0, 0, 0], [50, 25])
level.enemies = [[60, 8]]
level.enemies_health = [400]
# aaaaaaaaaaaaaaaaaaaaa

bossTick = 0
while True:
    key = screen.getch()

    killedBoss = False
    match key:
        case 258:  # move down
            if not level.player_pos[1] >= 26:
                killedBoss = level.movePlayerBoss([0, 1], player, levelNum)
            elif level.exits[3] == 1 and 51 < level.player_pos[0] < 57:
                killedBoss = level.movePlayerBoss([0, 1], player, level)
        case 259:  # move up
            if not level.player_pos[1] <= 6:
                killedBoss = level.movePlayerBoss([0, -1], player, levelNum)
            elif level.exits[2] == 1 and 51 < level.player_pos[0] < 57:
                killedBoss = level.movePlayerBoss([0, -1], player, levelNum)
        case 261:  # Move right
            if not level.player_pos[0] >= 102:
                killedBoss = level.movePlayerBoss([1, 0], player, levelNum)
            elif level.exits[0] == 1 and 12 < level.player_pos[1] < 18:
                killedBoss = level.movePlayerBoss([1, 0], player, levelNum)
        case 260:  # Move left
            if not level.player_pos[0] <= 6:
                killedBoss = level.movePlayerBoss([-1, 0], player, levelNum)
            elif level.exits[1] == 1 and 12 < level.player_pos[1] < 18:
                killedBoss = level.movePlayerBoss([-1, 0], player, levelNum)
        case 105: # key "i" - shows inventory
            player.showInventory()

    if killedBoss:
        break
    level.updateEnemies(True, ["down"])
    level.renderLevel(player, True)
    addGameInfo(player, key, tick, currentX, currentY)

    if bossTick % 10 == 0:
        for i in range(96):
            if random.randint(0, 5) != 3:
                level.enemies.append([6+i, 6])
                level.enemies_health.append(0)

    bossTick += 1
    tick += 1

screen.clear()

timeTaken = round(time.time() - initialTime)

add_str_center("You defeated the demon!", 14)
add_str_center("[ Contunue ]", 16, 18)

add_str_center("Final stats:", 10)
add_str_center(f"Score: {player.score}", 14)
add_str_center(f"Ticks taken: {tick}", 16)
add_str_center(f"Time taken: {timeTaken} seconds", 18)

add_str_center("[ quit ]", 20)
waitUntilEnter()
# the end yay :)

