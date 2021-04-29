from typing import Callable
from os.path import isfile, join as path_join

file_name = path_join('input', 'day06.txt')


def to_list(mf: Callable = int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]


def to_gen(mf: Callable = int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)


if not isfile(file_name):
	from aoc import get_input_file

	get_input_file()

instructions = open(file_name).read().strip().split("\n")


def part1():
	grid = [[0] * 1000 for i in range(1000)]

	for instr in instructions:
		parts = instr.split()
		if parts[0] == "toggle":
			lower = list(map(int, parts[1].split(",")))
			upper = list(map(int, parts[3].split(",")))

			for y in range(lower[1], upper[1] + 1):
				for x in range(lower[0], upper[0] + 1):
					grid[y][x] ^= 1

		elif parts[0] == "turn":
			lower = list(map(int, parts[2].split(",")))
			upper = list(map(int, parts[4].split(",")))
			if parts[1] == "on":
				set_value = [1] * (upper[0] - lower[0] + 1)
			else:
				set_value = [0] * (upper[0] - lower[0] + 1)

			for y in range(lower[1], upper[1] + 1):
				grid[y][lower[0]:upper[0] + 1] = set_value

	count = sum(map(sum, grid))

	return count


def part2():
	grid = [[0] * 1000 for i in range(1000)]

	for instr in instructions:
		parts = instr.split()
		if parts[0] == "toggle":
			lower = list(map(int, parts[1].split(",")))
			upper = list(map(int, parts[3].split(",")))

			for y in range(lower[1], upper[1] + 1):
				for x in range(lower[0], upper[0] + 1):
					grid[y][x] += 2

		elif parts[0] == "turn":
			lower = list(map(int, parts[2].split(",")))
			upper = list(map(int, parts[4].split(",")))
			if parts[1] == "on":
				diff = 1
			else:
				diff = -1

			for y in range(lower[1], upper[1] + 1):
				for x in range(lower[0], upper[0] + 1):
					grid[y][x] = max(0, grid[y][x] + diff)

	count = sum(map(sum, grid))

	return count


print(part1())
print(part2())
