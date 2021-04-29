from typing import Callable
from os.path import isfile, join as path_join

file_name = path_join('input', 'day18.txt')


def to_list(mf: Callable = int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]


def to_gen(mf: Callable = int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)


if not isfile(file_name):
	from aoc import get_input_file

	get_input_file()

grid_og = [list(line) for line in open(file_name).read().strip().split("\n")]

dirs = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, -1), (-1, 1), (1, -1)]


def part1():
	grid = [row[:] for row in grid_og]

	for i in range(100):
		grid_new = [row[:] for row in grid]

		for y in range(100):
			for x in range(100):
				adj = 0
				for dir in dirs:
					new_y = y + dir[0]
					new_x = x + dir[1]
					if 0 <= new_y < 100 and 0 <= new_x < 100:
						if grid[y + dir[0]][x + dir[1]] == "#":
							adj += 1

				if grid[y][x] == "#" and (adj < 2 or adj > 3):
					grid_new[y][x] = "."
				if grid[y][x] == "." and adj == 3:
					grid_new[y][x] = "#"

		grid = [row[:] for row in grid_new]

	count = 0
	for row in grid:
		count += row.count("#")

	return count


def part2():
	grid = [row[:] for row in grid_og]
	corners = [(0, 0), (0, 99), (99, 0), (99, 99)]
	for corner in corners:
		grid[corner[0]][corner[1]] = "#"

	for i in range(100):
		grid_new = [row[:] for row in grid]

		for y in range(100):
			for x in range(100):
				if (y, x) in corners:
					continue

				adj = 0
				for dir in dirs:
					new_y = y + dir[0]
					new_x = x + dir[1]
					if 0 <= new_y < 100 and 0 <= new_x < 100:
						if grid[y + dir[0]][x + dir[1]] == "#":
							adj += 1

				if grid[y][x] == "#" and (adj < 2 or adj > 3):
					grid_new[y][x] = "."
				if grid[y][x] == "." and adj == 3:
					grid_new[y][x] = "#"

		grid = [row[:] for row in grid_new]

	count = 0
	for row in grid:
		count += row.count("#")

	return count


print(part1())
print(part2())
