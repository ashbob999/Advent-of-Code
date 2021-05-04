from typing import Callable
from os.path import isfile, join as path_join

file_name = path_join('input', 'day07.txt')


def to_list(mf: Callable = int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]


def to_gen(mf: Callable = int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)


if not isfile(file_name):
	from aoc import get_input_file

	get_input_file(session_path=['..', '.env'])

data = to_list(mf=str, sep="\n")

rules = {}

for rule in data:
	rule = rule.replace(".", "")
	bs = rule.split("bag")[:-1]
	col1 = "".join(bs[0].strip().split(" "))

	cont = {}

	if bs[1].strip().split(" ")[-1] == "other":
		pass
	else:
		for b in bs[1:]:
			b = b.strip()
			bb = b.split(" ")
			if "contain" in bb:
				bb.remove("contain")

			col = "".join(bb[-2:])
			amnt = int(bb[1])
			cont[col] = amnt

	rules[col1] = cont

done = {}


def r(curr, tar):
	if curr in done:
		return done[curr]
	c = 0
	for t in rules[curr].keys():
		if t == tar:
			c = 1
			done[curr] = c
			return c
		else:
			c |= r(t, tar)

	done[curr] = c
	return c


def part1():
	cn = 0
	for t in rules.keys():
		if r(t, "shinygold"):
			cn += 1
	print(cn)


done2 = {}


def r2(curr):
	if curr in done2:
		return done2[curr]

	tot = sum(rules[curr].values())
	for t, a in rules[curr].items():
		tot += a * r2(t)

	done2[curr] = tot
	return tot


def part2():
	print(r2("shinygold"))


part1()
part2()
