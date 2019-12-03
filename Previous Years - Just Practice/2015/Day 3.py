# link to Day 1: https://adventofcode.com/2015/day/4

# splits the input file into a list of lines
with open("inputs/Day_3_Input.txt", "r") as file:
    lines = [line.strip() for line in file]

moves = lines[0]

# Part 1

locations = set()

start = (0, 0)
current_location = list(start)

locations.add(start)

for move in moves:
    if move == "^":  # increases Y
        current_location[1] = current_location[1] + 1
    elif move == "v":  # decreases Y
        current_location[1] = current_location[1] - 1
    elif move == "<":  # decreases X
        current_location[0] = current_location[0] - 1
    elif move == ">":  # increases X
        current_location[0] = current_location[0] + 1
    else:
        break
    locations.add(tuple(current_location))

print("Part 1: ", len(locations))

# Part 2

locations = set()

start = (0, 0)
current_location = list(start)
robo_current_location = list(start)

locations.add(start)

for i in range(0, len(moves), 2):
    move = moves[i]
    robo_move = moves[i + 1]

    if move == "^":  # increases Y
        current_location[1] = current_location[1] + 1
    elif move == "v":  # decreases Y
        current_location[1] = current_location[1] - 1
    elif move == "<":  # decreases X
        current_location[0] = current_location[0] - 1
    elif move == ">":  # increases X
        current_location[0] = current_location[0] + 1
    else:
        break
    locations.add(tuple(current_location))

    if robo_move == "^":  # increases Y
        robo_current_location[1] = robo_current_location[1] + 1
    elif robo_move == "v":  # decreases Y
        robo_current_location[1] = robo_current_location[1] - 1
    elif robo_move == "<":  # decreases X
        robo_current_location[0] = robo_current_location[0] - 1
    elif robo_move == ">":  # increases X
        robo_current_location[0] = robo_current_location[0] + 1
    else:
        break
    locations.add(tuple(robo_current_location))

print("Part 2: ", len(locations))
