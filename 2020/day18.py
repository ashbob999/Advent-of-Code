from typing import Callable
from os.path import isfile, join as path_join
file_name = path_join('input', 'day18.txt')
def to_list(mf: Callable = int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]
def to_gen(mf: Callable = int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)

if not isfile(file_name):
	from aoc import get_input_file
	get_input_file(session_path=['..', '.env'])


data = open(file_name).read().strip()

data = data.replace("(", " ( ")
data = data.replace(")", " ) ")

data = data.split("\n")
eq = []

for e in data:
	cd = 0
	eq.append([])
	for c in e.strip().split():
		if c.isnumeric():
			if cd == 0:
				eq[-1].append(int(c))
			elif cd == 1:
				eq[-1][-1].append(int(c))
			elif cd == 2:
				eq[-1][-1][-1].append(int(c))

		elif c in ("+", "*"):
			if cd == 0:
				eq[-1].append(c)
			elif cd == 1:
				eq[-1][-1].append(c)
			elif cd == 2:
				eq[-1][-1][-1].append(c)

		elif c == "(":
			if cd == 0:
				eq[-1].append([])
			elif cd == 1:
				eq[-1][-1].append([])
			cd += 1

		elif c == ")":
			cd -= 1


def se(e):
	e = e[:]

	i = 0

	for i in range(len(e)):
		if isinstance(e[i], list):
			e[i] = se(e[i])

	i = 0
	while len(e) > 1:
		if e[1] == "+":
			e[0:3] = [e[0] + e[2]]
		elif e[1] == "*":
			e[0:3] = [e[0] * e[2]]

	return e[0]

def part1():
	t = 0

	for e in eq:
		v = se(e)
		t += v

	print(t)


def se2(e_og):
	e = e_og[:]

	for i in range(len(e)):
		if isinstance(e[i], list):
			e[i] = se2(e[i])

	while len(e) > 1:
		if "+" in e:
			i = e.index("+")
			e[i-1:i+2] = [e[i-1] + e[i+1]]
		else:
			e[0:3] = [e[0] * e[2]]

	return e[0]


def part2():
	t = 0

	for e in eq:
		v = se2(e)
		t += v

	print(t)


part1()
part2()
