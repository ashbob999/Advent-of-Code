from typing import Callable
from os.path import isfile, join as path_join

file_name = path_join('input', 'day08.txt')


def to_list(mf: Callable = int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]


def to_gen(mf: Callable = int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)


if not isfile(file_name):
	from aoc import get_input_file

	get_input_file()

lines = open(file_name).read().strip().split("\n")


def part1():
	code_count = 0
	char_count = 0

	for line in lines:
		code_count += len(line)
		i = 0
		while i < len(line):
			if line[i] == "\\":
				if line[i + 1] == "\\" or line[i + 1] == '"':
					char_count += 1
					i += 1
				elif line[i + 1] == "x":
					char_count += 1
					i += 3
				else:
					char_count += 1
			else:
				char_count += 1
			i += 1

	char_count -= 2 * len(lines)
	return code_count - char_count


def part2():
	code_count = 0
	char_count = 0

	for line in lines:
		code_count += len(line)

		for c in line:
			if c in ('"', '\\',):
				char_count += 1
			char_count += 1

	char_count += 2 * len(lines)
	return char_count - code_count


print(part1())
print(part2())
