# link to Day 1: https://adventofcode.com/2015/day/2

# splits the input file into a list of lines
with open("inputs/Day_2_Input.txt", "r") as file:
    lines = [line.strip() for line in file]

presents = [list(map(int, line.split("x"))) for line in lines]


def calc_surface_area(length, width, height):
    return (2 * length * width) + (2 * width * height) + (2 * height * length)


def calc_slack_area(length, width, height):
    sides_1 = length * width
    sides_2 = width * height
    sides_3 = height * length

    return min(sides_1, sides_2, sides_3)


# Part 1

total_area = 0

for present in presents:
    total_area += calc_surface_area(present[0], present[1], present[2])
    total_area += calc_slack_area(present[0], present[1], present[2])

print("Part 1: ", total_area)


# Part 2

def calc_ribbon_length(length, width, height):
    perim_1 = 2 * length + 2 * width
    perim_2 = 2 * width + 2 * height
    perim_3 = 2 * length + 2 * height

    return min(perim_1, perim_2, perim_3)


def calc_bow_length(length, width, height):
    return length * width * height


ribbon_length = 0

for present in presents:
    ribbon_length += calc_ribbon_length(present[0], present[1], present[2])
    ribbon_length += calc_bow_length(present[0], present[1], present[2])

print("Part 2: ", ribbon_length)
