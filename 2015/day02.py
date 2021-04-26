from typing import Callable
from os.path import isfile, join as path_join
file_name = path_join('input', 'day02.txt')
def to_list(mf: Callable = int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]
def to_gen(mf: Callable = int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)

if not isfile(file_name):
	from aoc import get_input_file
	get_input_file()

presents = [list(map(int, line.split("x"))) for line in open(file_name).read().strip().split("\n")]

def calc_surface_area(length, width, height):
    return (2 * length * width) + (2 * width * height) + (2 * height * length)


def calc_slack_area(length, width, height):
    sides_1 = length * width
    sides_2 = width * height
    sides_3 = height * length

    return min(sides_1, sides_2, sides_3)

def part1():
    total_area = 0

    for present in presents:
        total_area += calc_surface_area(present[0], present[1], present[2])
        total_area += calc_slack_area(present[0], present[1], present[2])

    return total_area


def calc_ribbon_length(length, width, height):
    perim_1 = 2 * length + 2 * width
    perim_2 = 2 * width + 2 * height
    perim_3 = 2 * length + 2 * height

    return min(perim_1, perim_2, perim_3)


def calc_bow_length(length, width, height):
    return length * width * height


def part2():
    ribbon_length = 0

    for present in presents:
        ribbon_length += calc_ribbon_length(present[0], present[1], present[2])
        ribbon_length += calc_bow_length(present[0], present[1], present[2])

    return ribbon_length


print(part1())
print(part2())
