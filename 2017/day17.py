# @formatter:off
from os.path import isfile, join as path_join
from sys import path as sys_path
sys_path.insert(1, path_join(sys_path[0], '..'))
file_name = path_join('input', 'day17.txt')
def to_list(mf: object = int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]
def to_gen(mf: object = int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)
def p1(*args): ans = part1(*args); print(ans); return ans
def p2(*args): ans = part2(*args); print(ans); return ans

if not isfile(file_name):
	from aoc import get_input_file
	get_input_file(session_path=['..', '.env'])
# @formatter:on

from utils import parsefile

steps = parsefile(file_name, [int])[0]


def get_buffer(steps, times):
	buff = [0]
	index = 0

	for i in range(1, times + 1):
		index = (index + steps) % len(buff) + 1
		buff.insert(index, i)

	return buff


def part1():
	buff = get_buffer(steps, 2017)
	index = buff.index(2017)
	index = (index + 1) % len(buff)

	return buff[index]


def get_value_after_0_in_buffer(steps, times):
	buffer_length = 1
	index = 0
	last_value_in_pos_1 = None

	for i in range(1, times + 1):
		index = (index + steps) % buffer_length + 1
		if index == 1:
			last_value_in_pos_1 = i
		buffer_length += 1

	return last_value_in_pos_1


def part2():
	return get_value_after_0_in_buffer(steps, 50_000_000)


p1()
p2()
