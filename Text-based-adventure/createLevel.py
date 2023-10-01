import json
import os
import random

from consts import *
from gamePrints import *

class createLevel():
    def __init__(self, x, y, entryLoc, useOverride=False, exitOverides = [], playerOverride = []):
        self.exits = [0, 0, 0, 0] # right, left, up, down

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

            # Room overrides - basically just set cutom exits for stuff like
            # making the first room always have 4 exits
            if useOverride:
                self.exits = exitOverides

            # This just saves the exits we have created
            with open(f"saves/1/{x}_{y}", "w") as f:
                json.dump({"exits": self.exits}, f)

        # if the room already exits we can just check what is already saved.
        else:
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

        if playerOverride != []:
            self.player_pos = playerOverride


    def movePlayer(self, movement, player, level=1):
        '''move player, takes a list as input and adds that to player pos, and 
        also calculates damage to enemies'''
        self.player_pos[0] += movement[0]
        self.player_pos[1] += movement[1]

        # Check if hit enemies and calculate damage
        for count, i in enumerate(self.enemies):
            justAttacked = False
            if self.player_pos[0] in [i[0], i[0]+1] and self.player_pos[1]==i[1] and not(player.attacked_last):
                playerWeaponStats = weaponStats[player.weapon]
                weaponDamage = playerWeaponStats["base_dmg"] + random.randint(0, playerWeaponStats["modifier"])
                self.enemies_health[count] -= weaponDamage
                player.score += 10*level
                # make enemy die if health less than 0
                if self.enemies_health[count] <= 0:
                    self.enemies_health.pop(count)
                    self.enemies.pop(count)
                    player.score += 100*level
                    # Get stuff for killing enemy
                    if random.randint(0, 3) == 0:  # 1/4 chance to get health flask
                        if level == 1:
                            player.pickupItem("health flask I")
                        elif level == 2:
                            player.pickupItem("health flask II")
                        elif level == 3:
                            player.pickupItem("health flask III")
                        elif level == 4:
                            player.pickupItem("health flask IV")

                        player.last_message = "You killed the enemy and got a health flask"
                    else:  # 3/4 chance to get coins
                        coins = random.randint(2, 6)
                        player.pickupItem("coin", coins)
                        player.last_message = f"You killed the enemy and got {coins} coins"
                else:
                    player.last_message = f"You attacked the enemy and did {weaponDamage} damage"
                    player.attacked_last = True
            elif player.attacked_last:
                player.attacked_last = False
                attackDamage = random.randint(0, 5*level)
                player.health -= attackDamage
                player.last_message = f"The enemy attacked you and did {attackDamage} damage"


    def movePlayerBoss(self, movement, player, level=1):
        '''move player, takes a list as input and adds that to player pos, and 
        also calculates damage to enemies. This is a modified version for the
        boss fights'''

        totalBossHealth = level*200
        self.player_pos[0] += movement[0]
        self.player_pos[1] += movement[1]

        # So we can set last message
        attackedBoss = False

        # Boss coordinates (boss is index 0 in the list of enemies)
        bossX = self.enemies[0][0]
        bossY = self.enemies[0][1]


        # Checks if the player is touching the bos (the boss is a box so we need
        # to check around it to see if player is thouching it)
        if bossX-1 <= self.player_pos[0] <= bossX+1 and bossY-1 <= self.player_pos[1] <= bossY + 1:
            playerWeaponStats = weaponStats[player.weapon]
            weaponDamage = playerWeaponStats["base_dmg"] + random.randint(0, playerWeaponStats["modifier"])
            self.enemies_health[0] -= weaponDamage
            player.last_message = f"You did {weaponDamage} to the boss"

            player.score += 100*level

        # Return true if we killed the enemy
        if self.enemies_health[0] <= 0:
            return True

        # Check if hit enemies and calculate damage
        for count, i in enumerate(self.enemies):
            if count == 0: continue
            if self.player_pos[0] == i[0] and self.player_pos[1]==i[1]:
                damageTaken = random.randint(0, 3*level)
                player.last_message = f"You took {damageTaken} damage"
                player.health -= damageTaken
                attackedBoss = True

                # If its just one of the little things we just remove it after
                # it has damaged the player
                self.enemies_health.pop(count)
                self.enemies.pop(count)
                player.health -= level

        # Add the boss health to the screen if you didnt just attack the boss
        if not attackedBoss:
            bossHealth = self.enemies_health[0]
            player.last_message = f"Boss health: {bossHealth}/{totalBossHealth}"

        # otherwise return false
        return False


    def renderLevel(self, player, bossEnemies = False):
        '''Renders the level including player and enemies'''
        screen.clear()
        print_borders()

        # Add the walls for the level

        # top+bottom borders
        border = ''.join("#" for _ in range(106))
        for i in range(1, 6):
            screen.addstr(i, 1, border)
        for i in range(1, 6):
            screen.addstr(32-i, 1, border)

        # side borders
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
        if not bossEnemies:  # Normal room enemies (just use sad face)
            for i in self.enemies:
                screen.addstr(i[1], i[0], "☹", curses.color_pair(51))

        else:
            for count, i in enumerate(self.enemies):
                if count == 0:
                    # The boss is just a red box with a hole in the middle. 
                    # This renders that box
                    screen.addstr(i[1]-1, i[0]-1, "█▋▋", curses.color_pair(55))
                    screen.addstr(i[1], i[0]-1, "█▋▋", curses.color_pair(55))
                    screen.addstr(i[1]+1, i[0]-1, "▋▋█", curses.color_pair(55))

                    # And this renders the hole in the middle
                    screen.addstr(i[1], i[0], "█", curses.color_pair(11))
                else:
                    screen.addstr(i[1], i[0], "█", curses.color_pair(51))








        # add last message to screen for attacking and stuff
        if player.last_message != "":
            screen.addstr(3, 3, player.last_message)
            player.last_message = ""
        screen.refresh()


    def updateEnemies(self, usesBossOverride = False, BossOverrides = []):
        '''updates enemy positions'''
        # this is just horrible code
        if not usesBossOverride:
            for count, _ in enumerate(self.enemies):
                if random.randint(0, 1) == 1: # move in Y
                    if random.randint(0, 1) == 1:
                        if self.enemies[count][1] <= 24:

                            self.enemies[count][1] += 1
                        else:
                            self.enemies[count][1] -= 1
                    else:
                        if self.enemies[count][1] >= 8:
                            self.enemies[count][1] -= 1
                        else:
                            self.enemies[count][1] += 1
                else: # move in x
                    if random.randint(0, 1) == 1:
                        if self.enemies[count][0] <= 101:
                            self.enemies[count][0] += 1
                        else:
                            self.enemies[count][0] -= 1
                    else:
                        if self.enemies[count][0] >= 7:
                            self.enemies[count][0] -= 1
                        else:
                            self.enemies[count][0] += 1

        # This makes all enemies go down (for cool boss fight things)
        if "down" in BossOverrides: # this code makes pylint really unhappy
            for count, i in enumerate(self.enemies):
                # Index 0 means its the boss. This just uses the random enemy
                # movment. Moving towards the player would just make it too hard
                if count == 0:
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
                    continue

                self.enemies[count][1] += 1
                if i[1] == 27:
                    self.enemies.pop(count)
                    self.enemies_health.pop(count)




