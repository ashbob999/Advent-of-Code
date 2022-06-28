# @formatter:off
from os.path import isfile, join as path_join
from sys import path as sys_path
sys_path.insert(1, path_join(sys_path[0], '..'))
file_name = path_join('input', 'day06.txt')
def to_list(mf: object = int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]
def to_gen(mf: object = int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)
def p1(*args): ans = part1(*args); print(ans); return ans
def p2(*args): ans = part2(*args); print(ans); return ans

if not isfile(file_name):
	from aoc import get_input_file
	get_input_file(session_path=['..', '.env'])
# @formatter:on

from utils import parsefile

memory = parsefile(file_name, [int])


def part1():
	mem = memory[:]
	c = 0

	states = set()
	states.add(tuple(mem))

	while True:
		new_mem = mem[:]
		c += 1

		max_value = max(new_mem)
		index = new_mem.index(max_value)

		size = new_mem[index]
		new_mem[index] = 0

		for i in range(1, size + 1):
			new_mem[(index + i) % 16] += 1

		if tuple(new_mem) in states:
			return c

		states.add(tuple(new_mem))
		mem = new_mem


def part2():
	mem = memory[:]
	c = 0

	states = {tuple(mem): 0}

	while True:
		new_mem = mem[:]
		c += 1

		max_value = max(new_mem)
		index = new_mem.index(max_value)

		size = new_mem[index]
		new_mem[index] = 0

		for i in range(1, size + 1):
			new_mem[(index + i) % 16] += 1

		if tuple(new_mem) in states:
			return c - states[tuple(new_mem)]

		states[tuple(new_mem)] = c
		mem = new_mem


p1()
p2()
