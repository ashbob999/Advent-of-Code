from typing import Callable
from os.path import isfile, join as path_join

file_name = path_join('input', 'day13.txt')


def to_list(mf: Callable = int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]


def to_gen(mf: Callable = int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)


if not isfile(file_name):
	from aoc import get_input_file

	get_input_file()

from itertools import permutations as perm

people = {}

for line in open(file_name).read().strip().split("\n"):
	parts = line.split()
	val = int(parts[3]) if parts[2] == "gain" else -1 * int(parts[3])

	if parts[0] in people:
		people[parts[0]][parts[-1][:-1]] = val
	else:
		people[parts[0]] = {parts[-1][:-1]: val}


def get_happiness(people):
	indexes = {i: v for i, v in enumerate(people.keys())}

	happiness = 0
	for p in perm(range(len(indexes))):
		res = [indexes[i] for i in p]
		happ = 0

		for i in range(len(res) - 1):
			# print(res[i], res[i + 1])
			happ += people[res[i]][res[i + 1]]
			happ += people[res[i + 1]][res[i]]

		happ += people[res[0]][res[-1]]
		happ += people[res[-1]][res[0]]

		happiness = max(happiness, happ)

	return happiness


def part1():
	return get_happiness(people)


def part2():
	names = list(people.keys())

	for k in people.keys():
		people[k]["myself"] = 0

	people["myself"] = {name: 0 for name in names}

	return get_happiness(people)


print(part1())
print(part2())
