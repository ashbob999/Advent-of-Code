from typing import Callable
from os.path import isfile, join as path_join
file_name = path_join('input', 'day03.txt')
def to_list(mf: Callable = int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]
def to_gen(mf: Callable = int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)

if not isfile(file_name):
	from aoc import get_input_file
	get_input_file()

moves = open(file_name).read().strip()

def part1():
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

    return len(locations)


def part2():
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

    return len(locations)


print(part1())
print(part2())
