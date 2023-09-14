from gamePrints import add_str_center, waitUntilEnter
from consts import *

INV_ITEMS = 0
INV_COUNTS = 1

class newPlayer():
    def __init__(self):
        self.score = 0
        self.health = 100
        self.inventory = [[], []]
        self.weapon = ""


    def pickupItem(self, item, count=1):
        if not item in self.inventory[INV_ITEMS]:
            self.inventory[INV_ITEMS].append(item)
            self.inventory[INV_COUNTS].append(count)
            return 0

        item_index = self.inventory[INV_ITEMS].index(item)
        self.inventory[INV_COUNTS][item_index] += count


    def removeItem(self, item, count=1):
        item_index = self.inventory[INV_ITEMS].index(item)
        self.inventory[INV_COUNTS][item_index] -= count

        # Remove item if you run out of it
        if self.inventory[INV_COUNTS][item_index] == 0:
            self.inventory[INV_COUNTS].pop(item_index)
            self.inventory[INV_ITEMS].pop(item_index)

    def setWeapon(self, weapon):
        print(self.inventory)
        if weapon in self.inventory[INV_ITEMS]:
            self.weapon = weapon
            print(f"success: {weapon}")
        else:
            print(weapon)

    def showInventory(self):
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
                    break
        



