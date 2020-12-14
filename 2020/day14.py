from typing import Callable
from os.path import isfile, join as path_join
file_name = path_join('input', 'day14.txt')
def to_list(mf: Callable = int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]
def to_gen(mf: Callable = int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)

if not isfile(file_name):
	from aoc import get_input_file
	get_input_file(session_path=['..', '.env'])

data = to_list(mf=str)

max_n = (1 << 36) - 1

def part1():
	mem = {}

	mask = None

	for r in data:
		if r.startswith("mask"):
			v = r.split(" = ")
			mask = v[1]
		else:
			v = r.split(" = ")
			index = int(v[0][4:-1])
			num = int(v[1])

			for i, c in enumerate(mask):
				if c == "X":
					continue
				elif c == "1":
					num |= 1 << (36 - i - 1)
				else:
					num &= max_n ^ (1 << (36 -i -1))

			mem[index] = num

	print(sum(mem.values()))


from itertools import product

def part2():
	mem = {}

	mask = None

	for r in data:
		if r.startswith("mask"):
			v = r.split(" = ")
			mask = v[1]
		else:
			v = r.split(" = ")
			index = int(v[0][4:-1])
			num = int(v[1])

			poss = []

			x_indexes = []

			for i, c in enumerate(mask):
				if c == "0":
					continue
				elif c == "1":
					index |= 1 << (36 - i - 1)
				else:
					x_indexes.append(i)

			for c in product("01", repeat=len(x_indexes)):
				tmp = list(bin(index)[2:].rjust(36, "0"))
				for i, x_index in enumerate(x_indexes):
					tmp[x_index] = c[i]

				mem[int("".join(tmp), 2)] = num
				#poss.append(int("".join(tmp), 2))

			#for p in poss:
			#	mem[p] = num

	print(sum(mem.values()))


part1()
part2()
