import json
import os
import random

from consts import *
from gamePrints import *

class createLevel():
    def __init__(self, x, y, entryLoc):
        self.exits = [0, 0, 0, 0] # right, left, up, down

        self.exits[0] = random.randint(0, 1)
        self.exits[1] = random.randint(0, 1)
        self.exits[2] = random.randint(0, 1)
        self.exits[3] = random.randint(0, 1)
        self.exits = [1,1,1,1] # for testing
        if not os.path.exists(f"saves/1/{x}_{y}"):
            # check adjacent rooms for exits and add exit if there is one
            if os.path.exists(f"saves/1/{x+1}_{y}"):
                with open(f"saves/1/{x+1}_{y}", "r") as f:
                    lvljson = json.loads(f.read())
                if lvljson["exits"][2] == 1:
                    self.exits[1] = 1
            if os.path.exists(f"saves/1/{x-1}_{y}"):
                with open(f"saves/1/{x-1}_{y}", "r") as f:
                    lvljson = json.loads(f.read())
                if lvljson["exits"][1] == 1:
                    self.exits[2] = 1
            if os.path.exists(f"saves/1/{x}_{y+1}"):
                with open(f"saves/1/{x}_{y+1}", "r") as f:
                    lvljson = json.loads(f.read())
                if lvljson["exits"][4] == 1:
                    self.exits[3] = 1
            if os.path.exists(f"saves/1/{x}_{y-1}"):
                with open(f"saves/1/{x}_{y-1}", "r") as f:
                    lvljson = json.loads(f.read())
                if lvljson["exits"][3] == 1:
                    self.exits[4] = 1

            # Save level
            with open(f"saves/1/{x}_{y}", "w") as f:
                json.dump({"exits": self.exits}, f)

        # set enemy positions
        self.enemies = []
        self.enemies_health = []
        for _ in range(random.randint(1, 4)):
            self.enemies.append([random.randint(40, 80), random.randint(6, 20)])
            self.enemies_health.append(50)

        # set player pos. Format of player pos is [x, y]
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
        '''move player, takes a list as input and adds that to player pos'''
        self.player_pos[0] += movement[0]
        self.player_pos[1] += movement[1]

        # Check if hit enemies and calculate damage
        for count, i in enumerate(self.enemies):
            if self.player_pos[0]==i[0] and self.player_pos[1]==i[1]:
                playerWeaponStats = weaponStats[player.weapon]
                weaponDamage = playerWeaponStats["base_dmg"] + random.randint(0, playerWeaponStats["modifier"])
                self.enemies_health[count] -= weaponDamage

                # make enemy die if health less than 0
                if self.enemies_health[count] <= 0:
                    self.enemies_health.pop(count)
                    self.enemes.pop(count)


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

        # Add the exit paths
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
