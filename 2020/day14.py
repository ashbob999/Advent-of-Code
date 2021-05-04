from os.path import isfile, join as path_join
from typing import Callable

file_name = path_join('input', 'day14.txt')


def to_list(mf: Callable = int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]


def to_gen(mf: Callable = int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)


if not isfile(file_name):
	from aoc import get_input_file

	get_input_file(session_path=['..', '.env'])

data = open(file_name).read().strip().split("\n")

max_n = (1 << 36) - 1

mem_0 = {}
mem_1 = {}

parsed = []


def part1():
	mem = {}

	mask = None

	for r in data:
		if r.startswith("mask"):
			v = r.split(" = ")
			mask = v[1]
			parsed.append((0, mask))
		else:
			v = r.split(" = ")
			index = int(v[0][4:-1])
			num = int(v[1])
			parsed.append((1, index, num))

			for i, c in enumerate(mask):
				if c == "X":
					continue
				elif c == "1":
					if i not in mem_1:
						mem_1[i] = 1 << (35 - i)
					num |= mem_1[i]
				else:
					if i not in mem_0:
						mem_0[i] = ~(1 << (35 - i))
					num &= mem_0[i]

			mem[index] = num

	print(sum(mem.values()))


from itertools import product


def part2():
	global ct, cc
	mem = {}

	mask = None

	for p in parsed:
		if p[0] == 0:
			mask = p[1]
		else:
			_, index, num = p

			x_indexes = []

			for i, c in enumerate(mask):
				if c == "0":
					continue
				elif c == "1":
					index |= mem_1[i]
				# index |= 1 << (36 - i - 1)
				else:
					x_indexes.append(i)

			for c in product((0, 1), repeat=len(x_indexes)):
				val = index

				for i, x_index in enumerate(x_indexes):
					if c[i]:
						val &= mem_0[x_index]
					# val &= max_n ^ (1 << (36 - x_index -1))
					else:
						val |= mem_1[x_index]
				# val |= 1 << (36 - x_index -1)

				# print(val)
				mem[val] = num

	print(sum(mem.values()))


part1()
part2()
