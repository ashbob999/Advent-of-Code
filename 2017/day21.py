# @formatter:off
from builtins import print
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

from utils import parsefile, to_tuple

raw_rules = parsefile(file_name, [[[list, "/"], " => "], "\n"])

start_pattern = [[".", "#", "."], [".", ".", "#"], ["#", "#", "#"]]


def flip(patt, dir):
	if dir == 0:  # v
		return [patt[i] for i in range(len(patt) - 1, -1, -1)]
	elif dir == 1:  # h
		return [t[::-1] for t in patt]


def transpose(patt):
	return [x for x in zip(*patt)]


def rotate(patt, dir):
	if dir == 0:
		return patt
	if dir == 90:
		tile = transpose(patt)
		return flip(tile, 1)


rules = {}
for r in raw_rules:
	# we have a total of 8 possible rotations/flips per rule
	# og
	# flip h
	# flip v
	# flip h, flip v
	# r 90
	# r 90, flip h
	# r 90, flip v
	# r 90, flip h, flip v

	rules[to_tuple(r[0])] = r[1]
	rules[to_tuple(flip(r[0], 1))] = r[1]
	rules[to_tuple(flip(r[0], 0))] = r[1]
	rules[to_tuple(flip(flip(r[0], 1), 0))] = r[1]

	rot = rotate(r[0], 90)
	rules[to_tuple(rot)] = r[1]
	rules[to_tuple(flip(rot, 1))] = r[1]
	rules[to_tuple(flip(rot, 0))] = r[1]
	rules[to_tuple(flip(flip(rot, 1), 0))] = r[1]


def iterate(grid):
	new_grid = []
	if len(grid) % 2 == 0:  # split into 2x2
		for y in range(len(grid) // 2):
			for x in range(len(grid) // 2):
				mini_grid = [r[x * 2:x * 2 + 2] for r in grid[y * 2:y * 2 + 2]]
				out_grid = rules[to_tuple(mini_grid)]
				for y2 in range(len(out_grid)):
					y_pos = y * len(out_grid) + y2
					if len(new_grid) <= y_pos:
						new_grid.append([])
					new_grid[y_pos].extend(out_grid[y2])

	else:  # split into 3x3
		for y in range(len(grid) // 3):
			for x in range(len(grid) // 3):
				mini_grid = [r[x * 3:x * 3 + 3] for r in grid[y * 3:y * 3 + 3]]
				out_grid = rules[to_tuple(mini_grid)]
				for y2 in range(len(out_grid)):
					y_pos = y * len(out_grid) + y2
					if len(new_grid) <= y_pos:
						new_grid.append([])
					new_grid[y_pos].extend(out_grid[y2])

	return new_grid


def part1():
	patt = [r[:] for r in start_pattern]

	for i in range(5):
		patt = iterate(patt)

	c = 0
	for r in patt:
		for v in r:
			if v == "#":
				c += 1

	return c


def part2():
	patt = [r[:] for r in start_pattern]

	for i in range(18):
		patt = iterate(patt)

	c = 0
	for r in patt:
		for v in r:
			if v == "#":
				c += 1

	return c


p1()
p2()
