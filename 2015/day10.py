from typing import Callable
from os.path import isfile, join as path_join

file_name = path_join('input', 'day10.txt')


def to_list(mf: Callable = int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]


def to_gen(mf: Callable = int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)


if not isfile(file_name):
	from aoc import get_input_file

	get_input_file()

num = open(file_name).read().strip()


def step(s):
	new_s = ""
	i = 0
	while i < len(s):
		# find digit count
		count = 0
		while i + count < len(s) and s[i + count] == s[i]:
			count += 1

		new_s += str(count)
		new_s += s[i]

		i += count

	return new_s


def part1():
	global num
	for i in range(40):
		num = step(num)

	return len(num)


def part2():
	global num
	for i in range(10):
		num = step(num)

	return len(num)


print(part1())
print(part2())
