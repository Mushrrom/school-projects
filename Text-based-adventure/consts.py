'''A collection of constants for use in other places in code
'''
import sys

# curses library
try:
    import curses
except ModuleNotFoundError:
    print("Failed to import curses.")
    sys.exit(1)

# curses screen
screen = curses.initscr()

weaponStats = {
    "dagger": {
        "base_dmg": 10,
        "modifier": 4,
    },
    "stormbreaker blade": {
        "base_dmg": 10,
        "modifier": 35
    },
    "Bloodmoon Dagger": {
        "base_dmg": 20,
        "modifier": 10
    },
    "stick": {
        "base_dmg": 1,
        "modifier": 1
    }

}

# descriptions for items. The first item in the string is the item title,
# and each value of the description is a new line
itemDescriptions = {
    "test": ["test item", "line 1", "line 2", "line 3"],
    "test2": ["test item 2", "line 1 _ 111", "line 2 _ 111"],
    "stormbreaker blade": ["stormbreaker blade", "Base damage: 10", "modifier: 20"],
    "Bloodmoon Dagger": ["Bloodmoon Dagger", "Base damage: 20", "modifier: 10"],
    "stick": ["Stick", "base damage: 1", "modifier: 1",
              "There is nothing special about this item you made a bad choice"]
}
