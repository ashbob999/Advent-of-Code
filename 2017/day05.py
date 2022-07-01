# @formatter:off
from os.path import isfile, join as path_join
from sys import path as sys_path
sys_path.insert(1, path_join(sys_path[0], '..'))
file_name = path_join('input', 'day05.txt')
def to_list(mf: object = int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]
def to_gen(mf: object = int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)
def p1(*args): ans = part1(*args); print(ans); return ans
def p2(*args): ans = part2(*args); print(ans); return ans

if not isfile(file_name):
	from aoc import get_input_file
	get_input_file()
# @formatter:on

from utils import parsefile

jumps = parsefile(file_name, [int, "\n"])
jumps_length = len(jumps)


def part1():
	jps = jumps[:]

	c = 0

	i = 0
	while True:
		offset = jps[i]
		jps[i] += 1
		i += offset
		c += 1
		if i < 0 or i >= jumps_length:
			return c


def part2():
	jps = jumps[:]

	c = 0

	i = 0
	while True:
		offset = jps[i]
		if offset >= 3:
			jps[i] -= 1
		else:
			jps[i] += 1
		i += offset
		c += 1
		if i < 0 or i >= jumps_length:
			return c


p1()
p2()
