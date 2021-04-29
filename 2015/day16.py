from typing import Callable
from os.path import isfile, join as path_join

file_name = path_join('input', 'day16.txt')


def to_list(mf: Callable = int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]


def to_gen(mf: Callable = int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)


if not isfile(file_name):
	from aoc import get_input_file

	get_input_file()

aunts = {}

for i, line in enumerate(open(file_name).read().strip().split("\n")):
	start_index = line.index(":")

	values = line[start_index + 2:].split(", ")
	d = {v.split(": ")[0]: int(v.split(": ")[1]) for v in values}

	aunts[i + 1] = d

card_values = {"children": 3, "cats": 7, "samoyeds": 2, "pomeranians": 3, "akitas": 0, "vizslas": 0, "goldfish": 5,
               "trees": 3, "cars": 2, "perfumes": 1}


def matches(values: dict, use_ranges=False):
	for k, v in values.items():
		if k not in card_values:
			return False

		if use_ranges:
			if k in ("cats", "trees"):  # greater than
				if card_values[k] >= v:
					return False
			elif k in ("pomeranians", "goldfish"):  # fewer than
				if card_values[k] <= v:
					return False
			elif card_values[k] != v:
				return False
		else:
			if card_values[k] != v:
				return False

	return True


def part1():
	for i, values in aunts.items():
		if matches(values):
			return i


def part2():
	for i, values in aunts.items():
		if matches(values, True):
			return i


print(part1())
print(part2())
