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

from utils import parsefile

data = parsefile(file_name, [list, "\n"])
data = [list(map(int, r)) for r in data]

w = len(data[0])
h = len(data)

dir = [(0, -1), (0, 1), (1, 0), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]

def step(grid):
	nines = set()
	
	grid = [r[:] for r in grid]
	
	for y in range(h):
		for x in range(w):
			if grid[y][x] > 9:
				nines.add((x, y))
			else:
				grid[y][x] += 1
				
				if grid[y][x] > 9:
					nines.add((x, y))
	
	flashed = set()
	
	while len(nines) > 0:
		cn = list(nines)[0]
		nines.remove(cn)
		
		flashed.add(cn)
		
		for d in dir:
			nx = cn[0] + d[0]
			ny = cn[1] + d[1]
				
			if nx >= 0 and nx < w and ny >= 0 and ny < h:
				grid[ny][nx] += 1
				
				if grid[ny][nx] > 9 and (nx, ny) not in flashed:
					nines.add((nx, ny))

	c = 0
	for y in range(h):
		for x in range(w):
			if grid[y][x] > 9:
				grid[y][x] = 0
				c += 1
				
	return grid, c

def part1():
	grid = data
	c = 0
	for i in range(100):
		grid, cc = step(grid)
		c += cc
		
	return c


def part2():
	grid = data
	n = 1
	while True:
		grid, c = step(grid)
		if c == w*h:
			return n
			
		n += 1


p1()
p2()
