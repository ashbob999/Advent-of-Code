from typing import Callable
from os.path import isfile, join as path_join

file_name = path_join('input', 'day18.txt')


def to_list(mf: Callable = int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]


def to_gen(mf: Callable = int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)


if not isfile(file_name):
	from aoc import get_input_file

	get_input_file()


def part1():
	pass


def part2():
	pass


part1()
part2()
