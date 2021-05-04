from typing import Callable
from os.path import isfile, join as path_join

file_name = path_join('input', 'day17.txt')


def to_list(mf: Callable = int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]


def to_gen(mf: Callable = int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)


if not isfile(file_name):
	from aoc import get_input_file

	get_input_file(session_path=['..', '.env'])

data = to_list(mf=str)

w = len(data[0])
h = len(data)

poss3 = [(0, 0, 1), (0, 1, 0), (1, 0, 0), (0, 0, -1), (0, -1, 0), (-1, 0, 0), (0, 1, 1), (1, 1, 0), (1, 0, 1),
         (0, -1, -1), (-1, -1, 0), (-1, 0, -1), (0, -1, 1), (0, 1, -1), (-1, 1, 0), (1, -1, 0), (1, 0, -1), (-1, 0, 1),
         (1, 1, 1), (-1, -1, -1), (1, 1, -1), (1, -1, 1), (-1, 1, 1), (-1, -1, 1), (-1, 1, -1), (1, -1, -1)]

poss4 = []
for x in range(-1, 2):
	for y in range(-1, 2):
		for z in range(-1, 2):
			for w in range(-1, 2):
				poss4.append((x, y, z, w))

poss4.remove((0, 0, 0, 0))
print(len(poss4))


def cycle3(grid, n):
	for i in range(n):
		next_grid = set(grid)
		minx, maxx, miny, maxy, minz, maxz = [0] * 6

		for p in grid:
			minx = min(minx, p[0])
			maxx = max(maxx, p[0])
			miny = min(miny, p[1])
			maxy = max(maxy, p[1])
			minz = min(minz, p[2])
			maxz = max(maxz, p[2])

		# print(minx, miny, minz)
		# print(maxx, maxy, maxz)

		for x in range(minx - 1, maxx + 2):
			for y in range(miny - 1, maxy + 2):
				for z in range(minz - 1, maxz + 2):
					adj = 0
					# print(x ,y, z)
					for p in poss3:
						np = (x + p[0], y + p[1], z + p[2])
						if np in grid:
							adj += 1

					if (x, y, z) in grid and adj != 2 and adj != 3:
						next_grid.remove((x, y, z))

					if (x, y, z) not in grid and adj == 3:
						next_grid.add((x, y, z))

		grid = next_grid
	# print("size", len(grid))
	# print(grid)

	return grid


def part1():
	grid = set()
	for y, l in enumerate(data):
		for x, c in enumerate(l):
			if c == "#":
				grid.add((x, y, 0))

	# print(grid)

	grid = cycle3(grid, 6)

	print("ans", len(grid))


def cycle4(grid, n):
	for i in range(n):
		next_grid = set(grid)
		minx, maxx, miny, maxy, minz, maxz, minw, maxw = [0] * 8

		for p in grid:
			minx = min(minx, p[0])
			maxx = max(maxx, p[0])
			miny = min(miny, p[1])
			maxy = max(maxy, p[1])
			minz = min(minz, p[2])
			maxz = max(maxz, p[2])
			minw = min(minw, p[3])
			maxw = max(maxw, p[3])

		# print(minx, miny, minz)
		# print(maxx, maxy, maxz)

		for x in range(minx - 1, maxx + 2):
			for y in range(miny - 1, maxy + 2):
				for z in range(minz - 1, maxz + 2):
					for w in range(minw - 1, maxw + 2):
						adj = 0
						# print(x ,y, z)
						for p in poss4:
							np = (x + p[0], y + p[1], z + p[2], w + p[3])
							if np in grid:
								adj += 1

						if (x, y, z, w) in grid and adj != 2 and adj != 3:
							next_grid.remove((x, y, z, w))

						if (x, y, z, w) not in grid and adj == 3:
							next_grid.add((x, y, z, w))

		grid = next_grid
	# print("size", len(grid))
	# print(grid)

	return grid


def part2():
	grid = set()
	for y, l in enumerate(data):
		for x, c in enumerate(l):
			if c == "#":
				grid.add((x, y, 0, 0))

	# print(grid)

	grid = cycle4(grid, 6)

	print("ans", len(grid))


part1()
part2()
