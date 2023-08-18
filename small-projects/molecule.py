import functools

molecules = reversed(list(input("Enter molecule chain: ")))

# Constants
ATOM_NAMES = 0
ATOM_COUNTS = 1


element_list = [[],[]]
current_number = "-1" # pylint: disable=C0103
llast = ""
bracket_contents = [1]

for count, current_char in enumerate(molecules):
    # honestly the best way i could think of to check if value is int
    if current_char.isdigit():
        current_number = current_char + current_number if current_number != "-1" else current_char
        current_number_as_int = int(current_number)
        continue

    int_current_number = int(current_number)
    adj_current_number = int_current_number if int_current_number > 1 else 1

    # check if its a bracket and add/remove to the list of bracket numbers if it is
    match current_char:
        case ")":
            bracket_contents.append(adj_current_number)
            current_number = "-1"
            continue
        case "(":
            bracket_contents.clear()
            current_number = "-1"
            continue


    # For elements like He which have 2 letters and the second is always a lower case
    if current_char == current_char.lower():
        llast = current_char
        continue

    current_character = current_char+llast # gets the lower case for 2 letter elements

    # Check if element already exists and add to that index if it does
    if current_character in element_list[0]:
        element_list[ATOM_COUNTS][element_list[0].index(current_character)] += ((adj_current_number)
            * functools.reduce(lambda x, y: x*y, bracket_contents))

    # add element to list and set first value
    else:
        element_list[ATOM_NAMES].append(current_character)
        element_list[ATOM_COUNTS].append((int_current_number if int(current_number) >= 0 else 1)
            * functools.reduce(lambda x, y: x*y, bracket_contents))

    # reset values
    current_number = "-1"
    llast = ""


# print out all of the values from the list
for count, i in enumerate(element_list[0]):
    print(f"{i}: {element_list[1][count]}")

