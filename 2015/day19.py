from typing import Callable
from os.path import isfile, join as path_join

file_name = path_join('input', 'day19.txt')


def to_list(mf: Callable = int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]


def to_gen(mf: Callable = int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)


if not isfile(file_name):
	from aoc import get_input_file

	get_input_file()

import random

data = open(file_name).read().strip().split("\n\n")

data1 = ["""e => H
e => O
H => HO
H => OH
O => HH""", "HOH"]

molecule = data[1]
replacements = []

for line in data[0].split("\n"):
	parts = line.split("=>")

	find = parts[0].strip()
	replacement = parts[1].strip()

	replacements.append((find, replacement))

subs = set(map(lambda x: x[0], replacements))
replacements = sorted(replacements, key=len, reverse=True)


def part1():
	poss = set()

	for i in range(len(molecule)):
		for rep in replacements:
			if molecule[i:i + len(rep[0])] == rep[0]:
				poss.add(molecule[:i] + rep[1] + molecule[i + len(rep[0]):])

	return len(poss)


def part2(curr, target):
	count = 0

	while curr != target:
		rm = random.choice(replacements)

		if rm[1] in curr:
			curr = curr.replace(rm[1], rm[0], 1)
			count += 1

	return count


print(part1())
print(part2(molecule, "e"))
