# @formatter:off
from os.path import isfile, join as path_join
from sys import path as sys_path
sys_path.insert(1, path_join(sys_path[0], '..'))
file_name = path_join('input', 'day11.txt')
def to_list(mf: object = int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]
def to_gen(mf: object = int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)
def p1(*args): ans = part1(*args); print(ans); return ans
def p2(*args): ans = part2(*args); print(ans); return ans

if not isfile(file_name):
	from aoc import get_input_file
	get_input_file(session_path=['..', '.env'])
# @formatter:on

from utils import *

data = parsefile(file_name,  [list, "\n"])

def expand(grid_):
	row_empty = []
	col_empty = []
	
	grid = [[v for v in r] for r in grid_]
	
	for r in grid:
		row_empty.append("#" not in r)
	
	for x in range(len(grid[0])):
		is_empty = True
		for r in grid:
			if r[x] == "#":
				is_empty = False
				break
				
		col_empty.append(is_empty)
	
	for y in range(len(row_empty)):
		for x in range(len(col_empty)):
			if row_empty[y] or col_empty[x]:
				grid[y][x] = "e"
	
	return grid

def dist(p1, p2, mult, grid):
	x1, x2 = p1[0], p2[0]
	if x2 < x1:
		x1, x2 = x2, x1
	
	y1, y2 = p1[1], p2[1]
	if y2 < y1:
		y1, y2 = y2, y1
	
	d = 0
	
	for y in range(y1, y2):
		if grid[y][x1] == "e":
			d += mult
		else:
			d += 1
	
	for x in range(x1, x2):
		if grid[y1][x] == "e":
			d += mult
		else:
			d += 1
	
	return d

grid = expand(data)

galax = []

for y in range(len(grid)):
	for x in range(len(grid[y])):
		if grid[y][x] == "#":
			galax.append((x, y))


def part1():
	res = 0
	
	for i in range(len(galax)):
		for j in range(i+1, len(galax)):
			res += dist(galax[i], galax[j], 2, grid)
			
	return res


def part2():
	res = 0
	
	for i in range(len(galax)):
		for j in range(i+1, len(galax)):
			res += dist(galax[i], galax[j], 1000000, grid)
			
	return res


p1()
p2()
