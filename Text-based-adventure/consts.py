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
