def add_str_center(in_str, centerx=-1, y = 0, color = 1):
    '''a func that adds a string to the screen centered at a given location'''
    if centerx == -1:
        screen.addstr(y, term_width//2 - len(in_str)//2, in_str,
                      curses.color_pair(color))


def view_hs(scr_imp, cur_imp, tw_imp, term_height): # view high scores
    with open("highscores.csv", "r") as f:
        data = f.read().split("\n")
        data[0] = data[0].split(",")
        data[1] = data[1].split(",")
    global screen, curses, term_width
    screen = scr_imp
    curses = cur_imp
    term_width = tw_imp
    screen.clear()
    
    add_str_center("high scores:", -1, term_height//2-7)
    add_str_center(f"{data[0][0]} by {data[1][0]}", -1, term_height//2-4)
    add_str_center(f"{data[0][1]} by {data[1][1]}", -1, term_height//2-2)
    add_str_center(f"{data[0][2]} by {data[1][2]}",-1, term_height//2)
    add_str_center(f"{data[0][3]} by {data[1][3]}", -1, term_height//2+2)
    add_str_center(f"{data[0][4]} by {data[1][4]}", -1, term_height//2+4)
    screen.getch()
