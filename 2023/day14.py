# @formatter:off
from os.path import isfile, join as path_join
from sys import path as sys_path
sys_path.insert(1, path_join(sys_path[0], '..'))
file_name = path_join('input', 'day14.txt')
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

height = len(data)
width = len(data[0])

def shift_north(grid_):
	grid = [r[:] for r in grid_]
	
	for y in range(height):
		for x in range(width):
			if grid[y][x] != "O":
				continue
			
			for y2 in range(y-1, -1, -1):
				if grid[y2][x] == ".":
					grid[y2][x] = "O"
					grid[y2+1][x] = "."
				else:
					break
	
	return grid


def score(grid):
	s = 0
	
	for y in range(height):
		score = height - y
		s += grid[y].count("O") * score
		
	return s

def part1():
	grid = shift_north(data)
	
	s = 0
	
	return score(grid)

def rot_90_ac(grid_):
	# clock
	return [list(reversed(col)) for col in zip(*grid_)]

def cycle(grid_):
	grid = [r[:] for r in grid_]
	
	# north
	grid = shift_north(grid)
	
	# west
	grid = rot_90_ac(grid)
	grid = shift_north(grid)
	
	# south
	grid = rot_90_ac(grid)
	grid = shift_north(grid)
	
	# east
	grid = rot_90_ac(grid)
	grid = shift_north(grid)
	
	grid = rot_90_ac(grid)
	return grid

def part2():
	seen = {}
	grid = data
	cycle_vals = None
	grid_cycle = None
	
	target = 1_000_000_000
	
	i=0
	while i < target:
		g = to_tuple(grid)
		seen[g] = i
		grid = cycle(grid)
		g = to_tuple(grid)
		i += 1
		if g in seen:
			cycle_vals = (i, seen[g])
			grid_cycle = grid
			break

	cycle_length = cycle_vals[0] - cycle_vals[1]
	offset = cycle_vals[1]
	full_cycles = (target - offset) // cycle_length
	
	rem = target - full_cycles * cycle_length - offset

	for i in range(rem):
		grid = cycle(grid)
	
	return score(grid)


p1()
p2()
