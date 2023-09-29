import random

from gamePrints import add_str_center, waitUntilEnter
from consts import *

# constants
INV_ITEMS = 0
INV_COUNTS = 1

class newPlayer():
    def __init__(self):
        self.score = 0
        self.health = 100
        self.inventory = [[], []]
        self.weapon = ""  # current weapon
        self.has_killed = False  # check for if the player has killed an enemy before
        self.attacked_last = False  # If player attacks then enemy will attack next turn
        self.last_message = ""  # Last message - for attacking and stuff


    def pickupItem(self, item, count=1):
        '''Player pick up item. Takes the item and count of item (default count = 1)'''
        if not item in self.inventory[INV_ITEMS]:
            self.inventory[INV_ITEMS].append(item)
            self.inventory[INV_COUNTS].append(count)
            return 0

        item_index = self.inventory[INV_ITEMS].index(item)
        self.inventory[INV_COUNTS][item_index] += count


    def removeItem(self, item, count=1):
        '''Remove an item from the player's inventory. Takes item and count of item as input'''
        item_index = self.inventory[INV_ITEMS].index(item)
        self.inventory[INV_COUNTS][item_index] -= count

        # Remove item if you run out of it
        if self.inventory[INV_COUNTS][item_index] == 0:
            self.inventory[INV_COUNTS].pop(item_index)
            self.inventory[INV_ITEMS].pop(item_index)

    def setWeapon(self, weapon):
        '''set the player's weapon'''
        print(self.inventory)
        if weapon in self.inventory[INV_ITEMS]:
            self.weapon = weapon
            print(f"success: {weapon}")
        else:
            print(weapon)

    def showInventory(self):
        '''show the inventory menu. Includes all the logic for selecting items too'''
        # Vertical border is the edges of the inventory plus the line that
        # splits the list of items from the descriptions
        verticalBorder = '|' + ''.join(" " for _ in range(30)) + '|' + ''.join(" " for _ in range(67)) + "|"
        for i in range(25):
            add_str_center(verticalBorder, 4+i)

        horisontalBorder = "".join("-" for _ in range(97))
        add_str_center(horisontalBorder, 4)
        add_str_center(horisontalBorder, 28)

        invLength = len(self.inventory[INV_ITEMS])
        sel = 0
        while True:
            # Print the inventory items
            for count, i in enumerate(self.inventory[INV_ITEMS]):
                itemString = i + " : " + str(self.inventory[INV_COUNTS][count])
                # If item is current selection set colour to white bg else set
                # black bg
                colour = 18 if sel == count else 81
                screen.addstr(5+count, 8, itemString, curses.color_pair(colour))

            # clear item description area
            spaces = "".join(" " for _ in range(67))
            for i in range(5, 29):
                screen.addstr(i, 36, spaces)

            # itemDescriptions is just a JSON object of all items in the game
            # saved in consts.py
            selectedItemDesc =  itemDescriptions[self.inventory[INV_ITEMS][sel]]

            # item title
            screen.addstr(5, 36, selectedItemDesc[0], curses.A_UNDERLINE)
            # item description
            for count, i in enumerate(selectedItemDesc[1:]):
                screen.addstr(7+count, 36, i)

            # wait for an input to move cursor up or down or select an item
            match screen.getch():
                case 258:
                    if sel != invLength-1:
                        sel += 1
                case 259:
                    if sel != 0:
                        sel -= 1
                case 10:
                    # For selecting weapons
                    if self.inventory[INV_ITEMS][sel] in weaponStats:
                        self.setWeapon(self.inventory[INV_ITEMS][sel])
                        add_str_center(f"Equiped {self.inventory[INV_ITEMS][sel]}", 15)
                        screen.getch()
                    # For selecting health flasks
                    elif self.inventory[INV_ITEMS][sel].startswith("health flask "):
                        # Gets the value of the health flask
                        flaskLevel = self.inventory[INV_ITEMS][sel].replace("health flask ", "")

                        # Get amount to heal based on level of health flask
                        healAmount = 0
                        if flaskLevel == "I":
                            healAmount = random.randint(0, 25)
                        elif flaskLevel == "II":
                            healAmount = random.randint(0, 40)
                        elif flaskLevel == "III":
                            healAmount = random.randint(20, 50)
                        elif flaskLevel == "IV":
                            healAmount = random.randint(40, 70)

                        self.health += healAmount
                        self.health = min(self.health, 100)  # Dont allow health > 100

                        # Go back an item if the health flask is the last item
                        if sel == invLength-1:
                            sel -= 1

                        # Fix inventory UI if using the last health flask
                        if self.inventory[INV_COUNTS][sel] == 1:
                            # Remove 1 from inventory length so user cant 
                            # accidently crash the game by going down
                            invLength -= 1
                            # Clear place where health flask used to be (avoids things looking weird)
                            screen.addstr(5+sel, 8, "".join(" " for _ in range(27)))
                            # Clear last spot of inventory to avoid an item showing
                            # up twice
                            screen.addstr(5+invLength, 8, "".join(" " for _ in range(27)))

                        add_str_center(f"healed {healAmount} hp", 15)
                        self.removeItem(f"health flask {flaskLevel}", 1)
                        screen.getch()



                case 27:
                    break







