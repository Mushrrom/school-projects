import functools

molecules = reversed(list(input("Enter molecule chain: ")))

# Constants
ATOM_NAMES = 0
ATOM_COUNTS = 1

# Variables that are adjusted across iterations
element_list = [[],[]]
current_number = "-1" # pylint: disable=C0103
last_char = ""
bracket_contents = [1]

for count, current_char in enumerate(molecules):
    # If it's a number than add it to the current number, for numbers of elements
    if current_char.isdigit():
        current_number = current_char + current_number if current_number != "-1" else current_char
        continue

    int_current_number = int(current_number)
    adj_current_number = int_current_number if int_current_number > 1 else 1
    current_element = current_char+last_char # for 2 letter elements
    brackets_multiplied = functools.reduce(lambda x, y: x*y, bracket_contents)

    # check if its a bracket and add/remove to the list of bracket numbers if it is
    match current_char:
        case ")":
            bracket_contents.append(adj_current_number)
            current_number = "-1"
            continue
        case "(":
            bracket_contents.pop(-1)
            current_number = "-1"
            continue

    # For elements like He which have 2 letters and the second is always a lower case
    if current_char == current_char.lower():
        last_char = current_char
        continue

    # If the element already exists in the list of elements add it to that index
    if current_element in element_list[0]:
        current_element_index = element_list[0].index(current_element)
        element_list[ATOM_COUNTS][current_element_index] += adj_current_number * brackets_multiplied
    # If the element doesnt already exist in the list of elements than add that
    # element to the list
    else:
        element_list[ATOM_NAMES].append(current_element)
        element_list[ATOM_COUNTS].append(adj_current_number * brackets_multiplied)

    # reset values after the element is added to the list
    current_number = "-1"
    last_char = ""


# print out all of the values from the list
for count, i in enumerate(element_list[0]):
    print(f"{i}: {element_list[1][count]}")

