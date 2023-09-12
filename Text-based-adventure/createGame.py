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
        if weapon in self.inventory:
            self.weapon = weapon
    

