from typing import Callable
from os.path import isfile, join as path_join
file_name = path_join('input', 'day14.txt')
def to_list(mf: Callable = int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]
def to_gen(mf: Callable = int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)

if not isfile(file_name):
	from aoc import get_input_file
	get_input_file(session_path=['..', '.env'])

#data = to_list(mf=str)
data = open(file_name).read().strip().split("\n")

max_n = (1 << 36) - 1

mem_0 = {}
mem_1 = {}

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
					if i not in mem_1:
						mem_1[i] = 1 << (36 - i - 1)
					num |= mem_1[i]
				else:
					if i not in mem_0:
						mem_0[i] = ~(1 << (36 - i - 1))
					num &= mem_0[i]

			mem[index] = num

	print(sum(mem.values()))

from itertools import product

adata = """mask = 000000000000000000000000000000X1001X
mem[42] = 100
mask = 00000000000000000000000000000000X0XX
mem[26] = 1""".split("\n")

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
					index |= mem_1[i]
					#index |= 1 << (36 - i - 1)
				else:
					x_indexes.append(i)

			for c in product("01", repeat=len(x_indexes)):
				val = index

				for i, x_index in enumerate(x_indexes):
					if c[i] == "0":
						if x_index not in mem_1:
							mem_1[x_index] = 1 << (36 - x_index - 1)
						val |= mem_1[x_index]
						#val |= 1 << (36 - x_index -1)
					else:
						if x_index not in mem_0:
							mem_0[x_index] = ~(1 << (36 - x_index - 1))
						val &= mem_0[x_index]
						#val &= max_n ^ (1 << (36 - x_index -1))

				#print(val)
				mem[val] = num

	print(sum(mem.values()))

part1()
part2()
