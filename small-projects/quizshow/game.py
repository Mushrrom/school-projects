import json
import os
import random
global term_height
global term_width
term_height = os.get_terminal_size().lines
term_width = os.get_terminal_size().columns

def add_str_center(in_str, centerx=-1, y = 0, color = 0):
    '''a func that adds a string to the screen centered at a given location'''
    if centerx == -1:
        screen.addstr(y, term_width//2 - len(in_str)//2, in_str,
                      curses.color_pair(color))

def clear_row(row):
    screen.addstr(row, 0,str(''.join(' ' for _ in range(term_width))),
                  curses.color_pair(1))


def play_game(curses_imp, screen_imp):
    global screen, curses
    screen = screen_imp
    curses = curses_imp
    lives = 3
    questionsjson = json.loads(open("questions.json", "r").read())
    screen.clear()
    screen.refresh()
    while lives > 0:
        question = random.choice(questionsjson["results"])
        clear_row(5)
        add_str_center(question["question"], -1, 5, 1)
        
        screen.refresh()
        screen.getch()


