from typing import Callable
from os.path import isfile, join as path_join

file_name = path_join('input', 'day25.txt')


def to_list(mf: Callable = int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]


def to_gen(mf: Callable = int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)


if not isfile(file_name):
	from aoc import get_input_file

	get_input_file()

line = open(file_name).read().strip()
parts = line.split()

row = int(parts[15][:-1])
col = int(parts[17][:-1])

value_1 = 20151125
mult = 252533
mod = 33554393


def sum(n):
	return (n * (n + 1)) // 2


def sum_range(n, m):  # range from n -> n+m
	return (m * m + 2 * m * n + m) // 2


def part1():
	index = 1

	# get starting row value
	# sum of 1-n (inclusive) = (n*(n+1))/2
	# sum of 2-col (inclusive)
	# => (col*(col+1)/2 - 1
	old = """
	for i in range(2, col + 1):
		index += i
	"""
	val1 = sum(col) - 1
	index += val1

	# get starting col value
	# sum of n-m (inclusive) = sum(m) - sum(n-1)
	# sum of col-col+row (inclusive)
	# => sum(col+row-2) - sum(col-1)
	old = """
	for i in range(col, col + row - 1):
		index += i
	"""
	# index += sum(col + row - 2) - sum(col - 1)
	# index += sum(col + row - 2) - (val1 + 1 - col)
	index += sum_range(col - 1, row - 1)

	# value = value * mult % mod: x times => value * mult^x % mod
	value = (value_1 * pow(mult, index - 1, mod)) % mod

	return value


def part2():
	pass


print(part1())
print(part2())
