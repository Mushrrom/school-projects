import json
import os
import random

from consts import *
from gamePrints import *

class createLevel():
    def __init__(self, x, y, entryLoc, useOverride=False, exitOverides = []):
        self.exits = [0, 0, 0, 0] # right, left, up, down
        print("abv")

        # self.exits = [1,1,1,1] # for testing
        if not os.path.exists(f"saves/1/{x}_{y}"):
            # This absolute mess checks whether the adjacent rooms have already
            # Been saved, and if they have it gets what the exit is in that
            # room and then uses that to figure out what exits should be in the
            # current room. If there isnt another room then it just randomly
            # decides whether to put an exit at that location.
            if os.path.exists(f"saves/1/{x+1}_{y}"):  # room to the right
                with open(f"saves/1/{x+1}_{y}", "r") as f:
                    lvljson = json.loads(f.read())
                if lvljson["exits"][0] == 1:
                    self.exits[1] = 1
            else:
                self.exits[1] = random.randint(0, 1)

            if os.path.exists(f"saves/1/{x-1}_{y}"):  # room to the left
                with open(f"saves/1/{x-1}_{y}", "r") as f:
                    lvljson = json.loads(f.read())
                if lvljson["exits"][1] == 1:
                    self.exits[0] = 1
            else:
                self.exits[0] = random.randint(0, 1)

            if os.path.exists(f"saves/1/{x}_{y+1}"):  # room upwards
                with open(f"saves/1/{x}_{y+1}", "r") as f:
                    lvljson = json.loads(f.read())
                if lvljson["exits"][3] == 1:
                    self.exits[2] = 1
            else:
                self.exits[2] = random.randint(0, 1)

            if os.path.exists(f"saves/1/{x}_{y-1}"):  # room downwards
                with open(f"saves/1/{x}_{y-1}", "r") as f:
                    lvljson = json.loads(f.read())
                if lvljson["exits"][2] == 1:
                    self.exits[3] = 1
            else:
                self.exits[3] = random.randint(0, 1)

            # This just saves the exits we have created
            with open(f"saves/1/{x}_{y}", "w") as f:
                json.dump({"exits": self.exits}, f)

        # if the room already exits we can just check what is already saved.
        else:
            # Room overrides - basically just set cutom exits for stuff like
            # making the first room always have 4 exits
            if useOverride:
                self.exits = exitOverides

            with open(f"saves/1/{x}_{y}") as f:
                lvljson = json.loads(f.read())
                self.exits = lvljson["exits"]

        
        # set enemy positions
        self.enemies = []
        self.enemies_health = []
        for _ in range(random.randint(1, 4)):
            self.enemies.append([random.randint(40, 80), random.randint(6, 20)])
            self.enemies_health.append(50)

        # set player pos. Format of player pos is [x, y]. X starts at 0 for left
        # side of the screen and increases towards the right. Y starts at 0 for
        # the top of the screen and then increases going down. This is due to
        # how curses manages positions
        self.player_pos = [0, 0]
        if entryLoc == 0:  # enter from bottom
            self.player_pos = [54, 31]
        elif entryLoc == 1: # enter from top
            self.player_pos = [54, 2]
        elif entryLoc == 2: # enter from right
            self.player_pos = [107, 15]
        else: # enter from left
            self.player_pos = [2, 15]


    def movePlayer(self, movement, player):
        '''move player, takes a list as input and adds that to player pos, and 
        also calculates damage to enemies'''
        self.player_pos[0] += movement[0]
        self.player_pos[1] += movement[1]

        # Check if hit enemies and calculate damage
        for count, i in enumerate(self.enemies):
            if self.player_pos[0] in [i[0], i[0]+1] and self.player_pos[1]==i[1]:
                playerWeaponStats = weaponStats[player.weapon]
                weaponDamage = playerWeaponStats["base_dmg"] + random.randint(0, playerWeaponStats["modifier"])
                self.enemies_health[count] -= weaponDamage

                # make enemy die if health less than 0
                if self.enemies_health[count] <= 0:
                    self.enemies_health.pop(count)
                    self.enemies.pop(count)


    def renderLevel(self):
        '''Renders the level including player and enemies'''
        screen.clear()
        print_borders()

        # Add the walls for the level
        border = ''.join("#" for _ in range(106))
        for i in range(1, 6):
            screen.addstr(i, 1, border)
        for i in range(1, 6):
            screen.addstr(32-i, 1, border)
        border = "#####"
        for i in range(1, 31):
            screen.addstr(i, 1, border)
        for i in range(1, 31):
            screen.addstr(i, 103, border)

        # Add the exit paths if there is an exit
        if self.exits[0] == 1:
            for i in range(5):
                screen.addstr(13+i, 103, "     ")
        if self.exits[1] == 1:
            for i in range(5):
                screen.addstr(13+i, 1, "     ")
        if self.exits[2] == 1:
            for i in range(5):
                screen.addstr(1+i, 52, "     ")
        if self.exits[3] == 1:
            for i in range(5):
                screen.addstr(27+i, 52, "     ")

        # Add player to screen
        screen.addstr(self.player_pos[1], self.player_pos[0], "☺", curses.color_pair(31))

        # add enemies to screen
        for i in self.enemies:
            screen.addstr(i[1], i[0], "☹", curses.color_pair(51))

        screen.refresh()


    def updateEnemies(self):
        '''updates enemy positions'''
        # this is just horrible nesting
        for count, _ in enumerate(self.enemies):
            if random.randint(0, 1) == 1: # move in Y
                if random.randint(0, 1) == 1:
                    if self.enemies[count][1] <= 25:

                        self.enemies[count][1] += 1
                    else:
                        self.enemies[count][1] -= 1
                else:
                    if self.enemies[count][1] >= 7:
                        self.enemies[count][1] -= 1
                    else:
                        self.enemies[count][1] += 1
            else: # move in x
                if random.randint(0, 1) == 1:
                    if self.enemies[count][0] <= 102:
                        self.enemies[count][0] += 1
                    else:
                        self.enemies[count][0] -= 1
                else:
                    if self.enemies[count][0] >= 6:
                        self.enemies[count][0] -= 1
                    else:
                        self.enemies[count][0] += 1
