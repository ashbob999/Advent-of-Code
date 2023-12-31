# @formatter:off
from os.path import isfile, join as path_join
from sys import path as sys_path
sys_path.insert(1, path_join(sys_path[0], '..'))
file_name = path_join('input', 'day21.txt')
def to_list(mf: object = int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]
def to_gen(mf: object = int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)
def p1(*args): ans = part1(*args); print(ans); return ans
def p2(*args): ans = part2(*args); print(ans); return ans

if not isfile(file_name):
	from aoc import get_input_file
	get_input_file(session_path=['..', '.env'])
# @formatter:on

from utils import *

data = parsefile(file_name, [list, "\n"])

height = len(data)
width = len(data[0])

assert width == height
size = width

start = None
for y in range(height):
	for x in range(width):
		if data[y][x] == "S":
			start = (x, y)
			break
	if start:
		break

adj = ((0, 1), (0, -1), (1, 0), (-1, 0))

grid = [r[:] for r in data]


def step(gardens):
	next_gardens = set()

	for g in gardens:
		for ad in adj:
			nx = g[0] + ad[0]
			ny = g[1] + ad[1]

			if 0 <= nx < width and 0 <= ny < height:
				if grid[ny][nx] != "#":
					next_gardens.add((nx, ny))

	return next_gardens


def part1():
	gardens = set()
	gardens.add(start)

	for i in range(64):
		gardens = step(gardens)
	# print(i, vals[-1])

	g = [r[:] for r in grid]
	for garden in gardens:
		if g[garden[1] % height][garden[0] % width] == ".":
			g[garden[1] % height][garden[0] % width] = "O"

	return len(gardens)


def step2(gardens: set, not_gardens: set):
	gardens, not_gardens = not_gardens, gardens
	new_gardens = set()
	new_not_gardens = set()

	for g in gardens:
		for ad in adj:
			nx = g[0] + ad[0]
			ny = g[1] + ad[1]

			n = (nx, ny)

			if n not in new_gardens and n not in new_not_gardens:

				nxm = nx % width
				nym = ny % height

				if grid[nym][nxm] != "#":
					new_not_gardens.add(n)

	for g in not_gardens:
		for ad in adj:
			nx = g[0] + ad[0]
			ny = g[1] + ad[1]

			n = (nx, ny)

			if n not in new_gardens and n not in new_not_gardens:

				nxm = nx % width
				nym = ny % height

				if grid[nym][nxm] != "#":
					new_gardens.add(n)

	gardens |= new_gardens
	not_gardens |= new_not_gardens
	return new_gardens, new_not_gardens


def do_steps(gardens, not_gardens, steps):
	for i in range(steps):
		gardens, not_gardens = step2(gardens, not_gardens)
	return gardens, not_gardens


def part2():
	step_count = 26501365

	"""
	the target steps end on a border of the grids
	so steps % size == size // 2 

	at the end of each full grid size the number of gardens follows a quadratic sequence

	y = ax^2 + bx + c
	
	2a = 2nd diff
	3a + b = 1st diff (y[2] - y[1])
	a + b + c = y[1]
	"""

	full_count = step_count // size
	steps_to_edge_of_grid = size // 2

	rem = step_count % size

	assert rem == steps_to_edge_of_grid

	y_vals = []

	gardens = set()
	not_gardens = set()
	gardens.add(start)

	# do initial steps y[0]
	# gardens = do_steps(gardens, steps_to_edge_of_grid)
	gardens, not_gardens = do_steps(gardens, not_gardens, steps_to_edge_of_grid)
	y_vals.append(len(gardens))

	# y[1]
	# gardens = do_steps(gardens, size)
	gardens, not_gardens = do_steps(gardens, not_gardens, size)
	y_vals.append(len(gardens))

	# y[2]
	# gardens = do_steps(gardens, size)
	gardens, not_gardens = do_steps(gardens, not_gardens, size)
	y_vals.append(len(gardens))

	first_diffs = [y_vals[i + 1] - y_vals[i] for i in range(len(y_vals) - 1)]
	second_diffs = [first_diffs[i + 1] - first_diffs[i] for i in range(len(first_diffs) - 1)]

	a = second_diffs[0] / 2
	b = first_diffs[0] - 3 * a
	c = y_vals[0] - a - b

	def eq(x):
		return a * (x ** 2) + b * x + c

	for i, y in enumerate(y_vals, 1):
		assert eq(i) == y

	result = eq(full_count + 1)
	return int(result)


p1()
p2()
