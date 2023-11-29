import os
import math
import sys
# i love ansi escape codes
# btw this doesnt work in idle because of ansi escape codes

def ctf():
    '''convert celsius to farenheit'''
    # ansi escape codes really make this painful to read. I am sorry if you are
    # trying to read this
    try:
        temp = int(input("\n\n\n\x1b[38;2;252;171;100mEnter temperature in celsius:"
            " \x1b[38;2;185;227;198m"))
    except ValueError: 
        print("\x1b[38;2;250;113;116mError: please enter a number\u001b[0m")
        sys.exit(1)
    print(f"\n\x1b[38;2;89;201;165m{temp}°c in farenheit is {round((temp-32)*(5/9), 2)}°f\u001b[0m")


def trap():
    '''get trapezoid area'''
    print('''
    \033[21;38;2;216;30;91mTrapeziod side names:\u001b[0m\x1b[38;2;89;201;165m
                          a
                     ---------------
                    /      |         \\
               b  /        |height     \\ c
                /          |             \\
               ----------------------------
                            c

    ''')

    try:
        sidea = int(input("\x1b[38;2;252;171;100mEnter side a (cm): \x1b[38;2;185;227;198m"))
        sidec = int(input("\x1b[38;2;252;171;100mEnter side c (cm): \x1b[38;2;185;227;198m"))
        height = int(input("\x1b[38;2;252;171;100mEnter height (cm): \x1b[38;2;185;227;198m" ))
    except ValueError:
        print("\x1b[38;2;250;113;116mError: please enter a number\u001b[0m")
        sys.exit(1)

    diff = sidea-sidec
    diff = diff * -1 if diff < 0 else diff

    if sidea > sidec:
        diff = sidea-sidec
        area = height * (1/2) * diff + height*sidec
    else:
        diff = sidec-sidea
        area = height*1/2*diff + height*sidea

    print(f"\n\x1b[38;2;89;201;165mThe area of the Trapeziod is {area}cm\u00b2\033[0m")


def circ():
    '''get circle area'''
    try:
        rad = int(input("\n\n\n\x1b[38;2;252;171;100mEnter raduis (cm):\x1b[38;2;185;227;198m "))
    except ValueError:
        print("\x1b[38;2;250;113;116mError: please enter a number\u001b[0m")
        sys.exit(1)

    print(f"\n\x1b[38;2;89;201;165mRaduis is {math.pi * (rad**2)}cm\u00b2")


def main():
    # this checks if the program is running in IDLE. This is because IDLE
    # does not support ANSI escape codes :(
    if "idlelib" in sys.modules:
        print("This program does not work in idle shell. Please run it from"
              "terminal")
        sys.exit(1)

    os.system('cls' if os.name == 'nt' else 'clear')

    print('''
    \033[21;5;38;2;216;30;91mcalculator - Select mode\u001b[0m

    \x1b[38;2;89;201;165ma) Celsuis to farenheit
    \x1b[38;2;185;227;198mb) Trapeziod
    \x1b[38;2;89;201;165mc) circle
    \x1b[38;2;185;227;198md) quit
    ''')
    mode = input("\x1b[38;2;252;171;100mSelect mode:\x1b[38;2;185;227;198m ")

    if mode == "a":
        ctf()
    elif mode == "b":
        trap()
    elif mode == "c":
        circ()

    # ansi escape code 5 was the best thing invented for computers
    print("\n\n\033[21;5;38;2;128;7;175;53mThank you for playing!!\u001b[0m")


if __name__ == "__main__":
    main()


