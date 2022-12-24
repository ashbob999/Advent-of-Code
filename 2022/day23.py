# @formatter:off
from os.path import isfile, join as path_join
from sys import path as sys_path
sys_path.insert(1, path_join(sys_path[0], '..'))
file_name = path_join('input', 'day23.txt')
def to_list(mf: object = int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]
def to_gen(mf: object = int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)
def p1(*args): ans = part1(*args); print(ans); return ans
def p2(*args): ans = part2(*args); print(ans); return ans

if not isfile(file_name):
	from aoc import get_input_file
	get_input_file(session_path=['..', '.env'])
# @formatter:on

from utils import parsefile
data = parsefile(file_name, [str, "\n"])

grid_og = set()
for y, r in enumerate(data):
	for x, v in enumerate(r):
		if v == "#":
			grid_og.add((x, y))

def dirs():
	while True:
		yield [(-1, -1), (0, -1), (1, -1)]
		yield [(-1, 1), (0, 1), (1, 1)]
		yield [(-1, -1), (-1, 0), (-1, 1)]
		yield [(1, -1), (1, 0), (1, 1)]

dir = dirs()
eight = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]


def step(grid):
	new_grid = set()
	
	dir_check = [next(dir) for i in range(4)]
	next(dir)
	
	new_pos = {}
	moved = len(grid)
	
	for p in grid:
		if all((p[0]+d[0], p[1]+d[1]) not in grid for d in eight):
			new_pos[p] = p
			moved -= 1
		else:
			done=False
			for d in dir_check:
				if all((p[0]+dv[0], p[1]+dv[1]) not in grid for dv in d):
					np = (p[0]+d[1][0], p[1]+d[1][1])
					if np in new_pos:
						op =new_pos[np]
						if op is not None:
							new_pos[op] = op
						new_pos[p] = p
						new_pos[np] = None
					else:
						new_pos[np] = p
					
					done = True
					break
				
			if not done:
				new_pos[p] = p
	
	for k, v in new_pos.items():
		if v is not None:
			new_grid.add(k)

	return new_grid, moved

def part1():
	g = grid_og.copy()
	
	for i in range(10):
		g, moved = step(g)
		
	minx=1000000
	maxx=0
	miny=1000000
	maxy=0
	
	for p in g:
		minx = min(minx, p[0])
		maxx = max(maxx, p[0])
		miny = min(miny, p[1])
		maxy = max(maxy, p[1])
		
	c = 0
	
	print(minx, maxx, miny, maxy)
	print(maxx-minx+1, maxy-miny+1)
	
	for y in range(miny, maxy+1):
		for x in range(minx, maxx+1):
			if (x, y) not in g:
				c += 1
	
	return c


def part2():
	global dir
	dir = dirs()
	g = grid_og.copy()
	
	i=0
	while True:
		if i%50==0:print(i)
		g, moved = step(g)
		i += 1
		
		if moved == 0:
			return i


p1()
p2()
