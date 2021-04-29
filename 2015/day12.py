from typing import Callable
from os.path import isfile, join as path_join

file_name = path_join('input', 'day12.txt')


def to_list(mf: Callable = int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]


def to_gen(mf: Callable = int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)


if not isfile(file_name):
	from aoc import get_input_file

	get_input_file()

import json

raw = open(file_name).read().strip()

data = json.loads(raw)


def get_sum(obj, ignore=None):
	s = 0
	if isinstance(obj, list):
		for v in obj:
			if isinstance(v, list) or isinstance(v, dict):
				s += get_sum(v, ignore)
			elif isinstance(v, int):
				s += v
	elif isinstance(obj, dict):
		if ignore in obj.keys() or ignore in obj.values():
			return 0
		for k, v in obj.items():
			if isinstance(v, list) or isinstance(v, dict):
				s += get_sum(v, ignore)
			elif isinstance(v, int):
				s += v

	return s


def part1():
	return get_sum(data)


def part2():
	return get_sum(data, "red")


print(part1())
print(part2())
