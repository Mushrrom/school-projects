# Text based adventure game
My assesment task for my programming course, made using curses.

I have tried to explain all curses functions the first time they are used, however if they are still confusing the [curses documentation](https://docs.python.org/3/howto/curses.html) is very detailed. I can also explain anything that I have not sufficiently commented.

## How to play
Just run main.py from a command prompt. If on windows 11 you will need to run it from a administrator command prompt because for some reason the default windows 11 terminal doesn't like `curses.resize_term`. If you're on windows 10 you should be all good. I haven't tested on macos/linux but curses is intended for unix so it should work all fine.

To attack enemies you just need to run into them.

If you are running on windows you will need to install the `windows-curses` package.
### Main game controls
| Control | Action |
| ------ | ------ |
| Up arrow | Move up or select higher option in a menu |
| Down arrow | Move down or select lower option in a menu |
| Left arrow | Move left |
| Right arrow | Move right |
| I key | Open inventory |
| Enter | Select an option in a menu |

### Inventory controls
| Control | Action |
| ------ | ------ |
| Up arrow | Select higher item in inventory |
| Down arrow | Select lower item in inventory |
| Enter | Equip weapon or use item |
| Esc | Exit inventory |

## Understanding my project structure
It's a really bad project structure.
### Main.py
Sets up the game and is what runs. This contains what happens in the game. It is extremely poorly made and a lot of it is just copying the logic from earlier to add new boss fights and levels. Comments are also pretty bad for code that is repeated. So it's best to look at the first instance of something occuring to understand it.

### consts.py
Stores the curses+screen, along with item and weapon info

### createLevel.py
Stores all the logic for each room. Whenever a new room is entered it is saved as an object from the createLevel function. Stores enemies and player position. Handles player moving, updating enemies, attacking/being attacked by enemies, and rendering the room to the screen

### createPlayer.py
Stores the player. Keeps track of player score, inventory, health and current weapon. Contains logic for picking up/removing items, showing and interacting with the inventory, and setting the equiped weapon.

### gamePrints.py
A really bad name ik, has logic for printing stuff to the screen, like the border, game info, and adding a string to the center of the screen

## Other stuff
If you need proof that i actually made this check [the commit history](https://github.com/mushrrom/school-projects/commits), every commit starting with "text based adv" was for this project. I am also happy to explain any code :)
