from os.path import isfile, join as path_join
from typing import Callable

file_name = path_join('input', 'day05.txt')


def to_list(mf: Callable = int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]


def to_gen(mf: Callable = int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)


if not isfile(file_name):
	from aoc import get_input_file

	get_input_file(session_path=['..', '.env'])

from itertools import repeat

table = {
	70: "0",  # F -> 0
	66: "1",  # B -> 1
	76: "0",  # L -> 0
	82: "1"  # R -> 1
}

st = str.translate


def part1():
	print(max(map(int, open(file_name).read().strip().translate(table).split("\n"), repeat(2))))


def part2():
	seats = sorted(map(int, open(file_name).read().strip().translate(table).split("\n"), repeat(2)))
	for i in range(0, len(seats) - 1):
		if seats[i + 1] - seats[i] == 2:
			print(seats[i] + 1)
			return


part1()
part2()
