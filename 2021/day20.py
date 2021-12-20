from os.path import isfile, join as path_join
from sys import path as sys_path
sys_path.insert(1, path_join(sys_path[0], '..'))
file_name = path_join('input', 'day20.txt')
def to_list(mf: object = int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]
def to_gen(mf: object = int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)
def p1(*args): ans = part1(*args); print(ans); return ans
def p2(*args): ans = part2(*args); print(ans); return ans

if not isfile(file_name):
	from aoc import get_input_file
	get_input_file(session_path=['..', '.env'])

from utils import parsefile

algo, grid = parsefile(file_name, [str, [str, "\n"], "\n\n"])

points = {}

for y in range(len(grid)):
	for x in range(len(grid[0])):
		points[(x, y)] = grid[y][x] == "#"


def get_value(p, points, algo, flipped, bounds):
	bs = 0
	i=0
	if flipped:
		default = 1
	else:
		default = 0
	
	for yd in range(-1, 2):
		for xd in range(-1, 2):
			bs<<= 1
			point = (p[0]+xd, p[1]+yd)
			if bounds[0] <= point[0] <= bounds[1] and bounds[2] <= point[1] <= bounds[3]:
				if point in points:
					bs |= 1 if points[point] == 1 else 0
			else:
				bs |= default
			i += 1

	return algo[bs]


def apply(points, algo, flipped):
	new_points = {}
	
	min_x = min([p[0] for p in points.keys()])
	max_x = max([p[0] for p in points.keys()])
	min_y = min([p[1] for p in points.keys()])
	max_y = max([p[1] for p in points.keys()])
	
	bounds = [min_x, max_x, min_y, max_y]
	
	for y in range(min_y-1, max_y+2):
		for x in range(min_x-1, max_x+2):
			new_points[(x, y)] = get_value((x, y), points, algo, flipped, bounds) == "#"
	
	return new_points 

def part1():
	should_flip = algo[0] == "#"
	
	ps = points
	for i in range(2):
		ps = apply(ps, algo, should_flip and (i%2==1))
	
	return len([v for k, v in ps.items() if v])

def part2():
	should_flip = algo[0] == "#"
	
	ps = points
	for i in range(50):
		ps = apply(ps, algo, should_flip and (i%2==1))
	
	return len([v for k, v in ps.items() if v])


p1()
p2()
