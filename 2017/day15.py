# @formatter:off
from os.path import isfile, join as path_join
from sys import path as sys_path
sys_path.insert(1, path_join(sys_path[0], '..'))
file_name = path_join('input', 'day15.txt')
def to_list(mf: object = int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]
def to_gen(mf: object = int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)
def p1(*args): ans = part1(*args); print(ans); return ans
def p2(*args): ans = part2(*args); print(ans); return ans

if not isfile(file_name):
	from aoc import get_input_file
	get_input_file(session_path=['..', '.env'])
# @formatter:on

from utils import parsefile

gens = parsefile(file_name, [[None, 1, str, 1, None, 2, int, 1], "\n"])


def get_next_value(prev_value, factor):
	return (prev_value * factor) % 2147483647


def count_pairs(gen_a_start, gen_b_start, iterations):
	matches = 0

	value_a = gen_a_start
	value_b = gen_b_start

	for i in range(iterations):
		value_a = get_next_value(value_a, 16807)
		value_b = get_next_value(value_b, 48271)

		if value_a & 0xffff == value_b & 0xffff:
			matches += 1

	return matches


def part1():
	return count_pairs(gens[0][1], gens[1][1], 40_000_000)


def get_next_value2(prev_value, factor, div):
	value = (prev_value * factor) % 2147483647
	while value % div != 0:
		value = (value * factor) % 2147483647
	return value


def count_pairs2(gen_a_start, gen_b_start, iterations):
	matches = 0

	value_a = gen_a_start
	value_b = gen_b_start

	for i in range(iterations):
		value_a = get_next_value2(value_a, 16807, 4)
		value_b = get_next_value2(value_b, 48271, 8)

		if value_a & 0xffff == value_b & 0xffff:
			matches += 1

	return matches


def part2():
	return count_pairs2(gens[0][1], gens[1][1], 5_000_000)


p1()
p2()
