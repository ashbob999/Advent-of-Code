# @formatter:off
from os.path import isfile, join as path_join
from sys import path as sys_path
sys_path.insert(1, path_join(sys_path[0], '..'))
file_name = path_join('input', 'day09.txt')
def to_list(mf: object = int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]
def to_gen(mf: object = int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)
def p1(*args): ans = part1(*args); print(ans); return ans
def p2(*args): ans = part2(*args); print(ans); return ans

if not isfile(file_name):
	from aoc import get_input_file
	get_input_file(session_path=['..', '.env'])
# @formatter:on

from utils import parsefile

stream = parsefile(file_name, None)


def calc_score(stream, count_garbage=False):
	score = 0
	level = 1

	garbage_count = 0
	in_garbage = False

	i = 0
	while i < len(stream):
		if not in_garbage and stream[i] == '{':
			score += level
			level += 1
		elif not in_garbage and stream[i] == '}':
			level -= 1
		elif not in_garbage and stream[i] == '<':
			in_garbage = True
		elif stream[i] == '>':
			in_garbage = False
		elif in_garbage and stream[i] == '!':
			i += 1
		elif in_garbage:
			garbage_count += 1

		i += 1

	if count_garbage:
		return garbage_count
	else:
		return score


def part1():
	return calc_score(stream)


def part2():
	return calc_score(stream, True)


p1()
p2()
