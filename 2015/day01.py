from typing import Callable
from os.path import isfile, join as path_join
file_name = path_join('input', 'day01.txt')
def to_list(mf: Callable = int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]
def to_gen(mf: Callable = int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)

if not isfile(file_name):
	from aoc import get_input_file
	get_input_file()

instructions = open(file_name).read().strip()

def part1():
    total = 0

    for char in instructions:
        if char == "(":
            total += 1
        elif char == ")":
            total -= 1

    return total


def part2():
    index_at_basement = 0
    total = 0

    for i in range(0, len(instructions), 1):
        if instructions[i] == "(":
            total += 1
        elif instructions[i] == ")":
            total -= 1

        if total == -1:
            index_at_basement = i + 1  # first instruction is: index = 1
            break

    return index_at_basement


print(part1())
print(part2())
