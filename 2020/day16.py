from os.path import isfile, join as path_join
from typing import Callable

file_name = path_join('input', 'day16.txt')


def to_list(mf: Callable = int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]


def to_gen(mf: Callable = int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)


if not isfile(file_name):
	from aoc import get_input_file

	get_input_file(session_path=['..', '.env'])

data = open(file_name).read().strip().split("\n\n")

ranges = {}

for i, r in enumerate(data[0].split("\n")):
	r = r.split(": ")
	name = r[0]

	rs = []
	for rng in r[1].split(" or "):
		rs.append(tuple(map(int, rng.split("-"))))

	ranges[name] = rs

my_ticket = data[1].split("\n")[1].strip()

other_tickets = [val.strip() for val in data[2].strip().split("\n")[1:]]
other_tickets.append(my_ticket)

parsed_tickets = [list(map(int, t.split(","))) for t in other_tickets]

valid = set()
invalid = set()

from functools import reduce
from operator import concat


def part1():
	s = 0
	values = reduce(concat, parsed_tickets, [])

	for val in values:
		if val in valid:
			continue
		elif val in invalid:
			s += val
			continue

		v = False
		for rngs in ranges.values():
			for rng in rngs:
				if rng[0] <= val <= rng[1]:
					v = True
					break
			if v:
				break

		if v:
			valid.add(val)
		else:
			invalid.add(val)
			s += val

	print(s)


def part2():
	global my_ticket
	vt = []

	for t in parsed_tickets:
		tmps = set(t)
		if tmps & invalid:
			continue

		vt.append(t)

	new_vt = [None] * len(vt[0])
	for i in range(len(vt[0])):
		s = set()
		for t in vt:
			s.add(t[i])

		new_vt[i] = s

	poss = {i: [] for i in range(len(vt[0]))}

	for i in range(len(vt[0])):
		for name, rng in ranges.items():

			val = True
			for t in vt:
				val_range = False
				for rg in rng:
					if t[i] >= rg[0] and t[i] <= rg[1]:
						val_range = True
						break
				if not val_range:
					val = False
					break

			if val:
				poss[i].append(name)

	corr = [None] * len(vt[0])
	while None in corr:
		for k, v in poss.items():
			if len(v) == 1:
				rm_val = v[0]
				corr[k] = rm_val

				for k2 in poss.keys():
					if rm_val in poss[k2]:
						poss[k2].remove(rm_val)

				break

	p = 1

	for i, v in enumerate(corr):
		if v.startswith("departure"):
			p *= parsed_tickets[-1][i]

	print(p)


part1()
part2()
