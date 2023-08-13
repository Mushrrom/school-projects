import json


def add_str_center(in_str, centerx=-1, y = 0, color = 0):
    '''a func that adds a string to the screen centered at a given location'''
    if centerx == -1:
        screen.addstr(y, term_width//2 - len(in_str)//2, in_str,
                      curses.color_pair(color))


def get_user_input(input_name):
    screen.clear()
    add_str_center(input_name, -1, term_height//2-5, 1)
    boxDashes = ''.join("─" for _ in range(term_width-2))
    boxSpaces = "│" + ''.join(" " for _ in range(term_width-2)) + "│"
    
    screen.addstr(term_height//2 - 1, 0, f"┌{boxDashes}┐", curses.color_pair(1))
    screen.addstr(term_height//2, 0, boxSpaces, curses.color_pair(1))
    screen.addstr(term_height//2 + 1, 0, f"└{boxDashes}┘", curses.color_pair(1))
    

    index = 1
    strn = ""
    while True:
        char = screen.getch()
        if char == 10: # enter
            break
        if char == 8: # delete
            if index > 0:
                index -= 1
                strn = strn[:-1]
                screen.addstr(term_height//2, index, " ")
        elif ((32<=char<=33 or 35<=char<=38 or 40<=char<=43 or 45<=char<=127)
            and index <term_width-1):
            strn += chr(char)
            screen.addstr(term_height//2, index, chr(char), curses.color_pair(1))
            index += 1

    return strn

def create_question(curses_imp, screen_imp, th_imp, tw_imp): # make question
    global curses, screen, term_height, term_width
    curses = curses_imp
    screen = screen_imp
    term_height = th_imp
    term_width = tw_imp

    q_title = str(get_user_input("Enter question name"))
    q_right = str(get_user_input("Enter correct answer"))
    q_wrong = []
    q_wrong.append(str(get_user_input("Enter wrong answer #1")))
    q_wrong.append(str(get_user_input("Enter wrong answer #2")))
    q_wrong.append(str(get_user_input("Enter wrong answer #3")))


    qjson = {"category": "custom",
             "question": q_title,
             "correct_answer": q_right,
             "incorrect_answers":q_wrong}

    with open("questions.json", "r") as f:
        data = json.loads(f.read())

    data["results"].append(qjson)

    with open("questions.json", "w") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    screen.clear()
    add_str_center("Created question :)", -1, term_height//2, 1)

if __name__ == "__main__":
    print("Please run main.py")
