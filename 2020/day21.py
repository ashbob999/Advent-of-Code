from typing import Callable
from os.path import isfile, join as path_join

file_name = path_join('input', 'day21.txt')


def to_list(mf: Callable = int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]


def to_gen(mf: Callable = int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)


if not isfile(file_name):
	from aoc import get_input_file

	get_input_file(session_path=['..', '.env'])

data = to_list(mf=str)

meals = []
ings_count = {}
poss_allers = {}

for d in data:
	ings = d.split(" (")[0].split(" ")

	if "(" in d:
		aller = d.split("contains")[1].replace(",", " ")
		aller = aller[:-1].split()
	else:
		aller = []

	for i in ings:
		if i in ings_count:
			ings_count[i] += 1
		else:
			ings_count[i] = 1
	for a in aller:
		if a in poss_allers:
			poss_allers[a] &= set(ings)
		else:
			poss_allers[a] = set(ings)

	meals.append((set(ings), set(aller)))

# print(poss_allers)

all_ings = set()
all_allers = set()

for m in meals:
	all_ings |= m[0]
	all_allers |= m[1]

aller_match = {k: None for k in all_allers}


def part1():
	while True:
		changed = False

		for k, v in poss_allers.items():
			if len(v) == 1:
				changed = True

				ing = list(v)[0]
				aller_match[k] = ing

				for k2 in poss_allers.keys():
					poss_allers[k2].discard(ing)

		if changed == 0:
			break

	# print(aller_match)

	c_ = 0
	for i, c in ings_count.items():
		if i not in aller_match.values():
			c_ += c

	print(c_)


def part2():
	ings = list(aller_match.values())
	rev_match = {}
	for k, v in aller_match.items():
		rev_match[v] = k

	ings = sorted(ings, key=lambda x: rev_match[x])

	cdi = ",".join(ings)

	print(cdi)


part1()
part2()
