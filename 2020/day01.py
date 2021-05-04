from typing import Callable
from os.path import isfile, join as path_join

file_name = path_join('input', 'day01.txt')


def to_list(mf: Callable = int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]


def to_gen(mf: Callable = int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)


if not isfile(file_name):
	from aoc import get_input_file

	get_input_file(session_path=['..', '.env'])

data = to_gen()

data = sorted(data)

s = set(data)


def part1():
	for v1 in data:
		rem = 2020 - v1
		if rem in s:
			return v1 * rem


def part2():
	for i in range(0, len(data)):
		for j in range(i + 1, len(data)):
			rem = 2020 - data[i] - data[j]
			if rem in s:
				return data[i] * data[j] * rem


print(part1())
print(part2())
