# @formatter:off
from os.path import isfile, join as path_join
from sys import path as sys_path
sys_path.insert(1, path_join(sys_path[0], '..'))
file_name = path_join('input', 'day04.txt')
def to_list(mf: object = int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]
def to_gen(mf: object = int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)
def p1(*args): ans = part1(*args); print(ans); return ans
def p2(*args): ans = part2(*args); print(ans); return ans

if not isfile(file_name):
	from aoc import get_input_file
	get_input_file()
# @formatter:on

from utils import parsefile

passwords = parsefile(file_name, [[str], "\n"])


def part1():
	c = 0

	for p in passwords:
		if len(p) == len(set(p)):
			c += 1

	return c


def part2():
	c = 0

	for p in passwords:
		p = list(map(frozenset, p))
		if len(p) == len(set(p)):
			c += 1

	return c


p1()
p2()
