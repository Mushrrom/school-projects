import json
import os
import random
from textstrs import *
global term_height
global term_width
term_height = os.get_terminal_size().lines
term_width = os.get_terminal_size().columns

def add_str_center(in_str, centerx=-1, y = 0, color = 0):
    '''a func that adds a string to the screen centered at a given location'''
    if centerx == -1:
        screen.addstr(y, term_width//2 - len(in_str)//2, in_str,
                      curses.color_pair(color))

def add_str_center_underlined(in_str, centerx=-1, y = 0, color = 0):
    '''a func that adds a string to the screen centered at a given location'''
    if centerx == -1:
        screen.addstr(y, term_width//2 - len(in_str)//2, in_str,
                      curses.color_pair(color) | curses.A_UNDERLINE)

def clear_row(row):
    screen.addstr(row, 0,str(''.join(' ' for _ in range(term_width))),
                  curses.color_pair(1))

def bottom_text():
    screenBottomLine = ''.join("─" for _ in range(term_width))
    screenBottomLine = list(screenBottomLine)
    screenBottomLine[20] = "┬"
    screenBottomLine = ''.join(screenBottomLine)
    screen.addstr(term_height-2, 0, screenBottomLine, curses.color_pair(1))

    screen.addstr(term_height-1, 0, "lives: ", curses.color_pair(1))
    screen.addstr(term_height-1, 7,
                  ''.join('♥ ' for _ in range(lives)),
                  curses.color_pair(3))
    screen.addstr(term_height-1, lives*2 + 7,
                  ''.join('♥ ' for _ in range(5-lives)),
                  curses.color_pair(4))
    screen.addstr(term_height-1, 20, "│", curses.color_pair(1))

    screen.addstr(term_height-1, 21, f" score: {score}", curses.color_pair(1))

def play_game(curses_imp, screen_imp):
    global screen, curses, score, lives
    screen = screen_imp
    curses = curses_imp
    lives = 3
    score = 0
    questionsjson = json.loads(open("questions.json", "r").read())
    screen.clear()
    screen.refresh()



    while lives > 0:
        question = random.choice(questionsjson["results"])
        screen.clear()

        # Varibles for making the question box
        qLength = len(question["question"])
        boxSpaces = ''.join(" " for _ in range(qLength+4))
        boxDashes = ''.join("─" for _ in range(qLength+4))

        # print question box
        add_str_center(f"┌{boxDashes}┐", -1, term_height//2 - 13, 1)
        add_str_center(f"│{boxSpaces}│", -1, term_height//2 - 12, 1)
        add_str_center(f"│{boxSpaces}│", -1, term_height//2 - 11, 1)
        add_str_center_underlined(question["category"], -1, term_height//2 - 11, 1)
        add_str_center(f"│{boxSpaces}│", -1, term_height//2 - 10, 1)
        add_str_center(f"│{boxSpaces}│", -1, term_height//2 - 9, 1)
        add_str_center(f"│  {question['question']}  │", -1, term_height//2 - 8, 1)
        add_str_center(f"│{boxSpaces}│", -1, term_height//2 - 7, 1)
        add_str_center(f"└{boxDashes}┘", -1, term_height//2 - 6, 1)

        # get info about the answers
        answers = question["incorrect_answers"]
        answers.append(question["correct_answer"])
        random.shuffle(answers)
        correctIndex = answers.index(question["correct_answer"])

        for count, i in enumerate(answers):
            answers[count] = f"[  {i}  ]"

        # add answers to screen
        add_str_center(answers[0], -1, (term_height//2)-3, 2)
        add_str_center(answers[1], -1, (term_height//2)-1, 1)
        add_str_center(answers[2], -1, (term_height//2)+1, 1)
        add_str_center(answers[3], -1, (term_height//2)+3, 1)

        # cheat
        add_str_center(str(correctIndex), -1, 1, 1)
        bottom_text()
        # select option (see line 102 of main.py for more info)
        sel = 0
        while True:
            char = screen.getch()

            if char == 258 and sel != 3:
                add_str_center(answers[sel], -1, (term_height//2)-3+(2*sel), 1)
                sel += 1
                add_str_center(answers[sel], -1, (term_height//2)-3+(2*sel), 2)
            elif char == 259 and sel != 0:
                add_str_center(answers[sel], -1, (term_height//2)-3+(2*sel), 1)
                sel -= 1
                add_str_center(answers[sel], -1, (term_height//2)-3+(2*sel), 2)
            elif char == 10:
                break
        
        # Correct :)
        if sel == correctIndex:
            score += 1
            screen.clear()
            
            for count, i in enumerate(correctText.split("\n")):
                add_str_center(i, -1, term_height//2-4+count, 1)

            bottom_text()
            screen.getch()
        else:
            
            
        screen.getch()


