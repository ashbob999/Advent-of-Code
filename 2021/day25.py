from os.path import isfile, join as path_join
from sys import path as sys_path
sys_path.insert(1, path_join(sys_path[0], '..'))
file_name = path_join('input', 'day25.txt')
def to_list(mf: object = int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]
def to_gen(mf: object = int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)
def p1(*args): ans = part1(*args); print(ans); return ans
def p2(*args): ans = part2(*args); print(ans); return ans

if not isfile(file_name):
	from aoc import get_input_file
	get_input_file(session_path=['..', '.env'])

from utils import parsefile

grid = parsefile(file_name, [[str, ""], "\n"])

w = len(grid[0])
h = len(grid)

def wrap(x, y):
	if x == w:
		return 0, y
	elif y == h:
		return x, 0
	return x, y

def step(grid):
	changed = 0
	
	ng = [v[:] for v in grid]
	
	# horizontal
	for y in range(h):
		for x in range(w):
			if grid[y][x] == ">":
				nx = x+1
				ny = y
				nx, ny = wrap(nx, ny)
			
				if grid[ny][nx] == ".":
					ng[y][x] = "."
					ng[ny][nx] = ">"
					changed += 1
	
	grid = ng
	ng = [v[:] for v in grid]
	
	# vertical
	for y in range(h):
		for x in range(w):
			if grid[y][x] == "v":
				nx = x
				ny = y+1
				nx, ny = wrap(nx, ny)
			
				if grid[ny][nx] == ".":
					ng[y][x] = "."
					ng[ny][nx] = "v"
					changed += 1
	
	return ng, changed

def part1():
	g = grid
	c=1
	s = 0
	
	while c > 0:
		g, c = step(g)
		s += 1
		
	return s


def part2():
	pass


p1()
p2()
