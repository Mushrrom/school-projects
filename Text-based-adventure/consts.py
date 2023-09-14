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
    }
}

itemDescriptions = {
    "test": ["test item", "line 1", "line 2", "line 3"],
    "test2": ["test item 2", "line 1 _ 111", "line 2 _ 111"]
}
