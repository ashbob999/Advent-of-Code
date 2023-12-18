# @formatter:off
from os.path import isfile, join as path_join
from sys import path as sys_path
sys_path.insert(1, path_join(sys_path[0], '..'))
file_name = path_join('input', 'day18.txt')
def to_list(mf: object = int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]
def to_gen(mf: object = int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)
def p1(*args): ans = part1(*args); print(ans); return ans
def p2(*args): ans = part2(*args); print(ans); return ans

if not isfile(file_name):
	from aoc import get_input_file
	get_input_file(session_path=['..', '.env'])
# @formatter:on

from utils import *

data = parsefile(file_name,  [[str, 1, int, 1, str], "\n"])

dirs = {
	"L": (-1, 0),
	"R": (1, 0),
	"U": (0, -1),
	"D": (0, 1)
}

def fill(grid, top_left, width, height, start):
	if start in grid:
		return set()
	
	to_check = []
	found = set()
	to_check.append(start)
	
	while len(to_check) > 0:
		curr = to_check.pop(0)
		found.add(curr)
		
		for dir in dirs.values():
			nx = curr[0] + dir[0]
			ny = curr[1] + dir[1]
			
			if top_left[0] <= nx < top_left[0] + width:
				if top_left[1] <= ny < top_left[1] + height:
					n = (nx, ny)
					if n not in grid and n not in found and n not in to_check:
						to_check.append(n)
					
	return found


def part1():
	grid = set()
	path = []
	start = (0, 0)
	curr = start
	grid.add(curr)
	path.append(curr)
	
	for d in data:
		dir = dirs[d[0]]
		amnt = d[1]
		
		for i in range(amnt):
			curr = (curr[0]+dir[0], curr[1]+dir[1])
			grid.add(curr)
			path.append(curr)
	
	minx = min(map(lambda v:v[0], grid))
	maxx = max(map(lambda v:v[0], grid))
	
	miny = min(map(lambda v:v[1], grid))
	maxy = max(map(lambda v:v[1], grid))
	
	width = maxx - minx +1
	height = maxy - miny +1
	top_left = (minx, miny)
	
	outside = set()
	
	# top
	for x in range(width):
		p = (top_left[0] + x, top_left[1])
		if p not in outside:
			outside |= fill(grid, top_left, width, height, p)
		
	# bottom
	for x in range(width):
		p = (top_left[0] + x, top_left[1] + height - 1)
		if p not in outside:
			outside |= fill(grid, top_left, width, height, p)
	
	# left
	for y in range(height):
		p = (top_left[0], top_left[1] + y)
		if p not in outside:
			outside |= fill(grid, top_left, width, height, p)
			
	# right
	for y in range(height):
		p = (top_left[0] + width - 1, top_left[1] + y)
		if p not in outside:
			outside |= fill(grid, top_left, width, height, p)

	return width*height - len(outside)


# shoelace formula
def polygonArea(polygon):
	# Initialize area
	area = 0.0
	
	# Calculate value of shoelace formula
	j = len(polygon) - 1
	for i in range(0,len(polygon)):
		area += (polygon[j][0] + polygon[i][0]) * (polygon[j][1] - polygon[i][1])
		j = i # j is previous vertex to i
	
	# Return absolute value
	return int(abs(area / 2.0))


def part2():
	path = []
	start = (0, 0)
	curr = start
	path.append(curr)
	
	boundary = 0
	
	for d in data:
		rgb = d[2][2:-1]
		
		dir_num = int(rgb[-1], 16)
		if dir_num == 0:
			dir = dirs["R"]
		elif dir_num == 1:
			dir = dirs["D"]
		elif dir_num == 2:
			dir = dirs["L"]
		elif dir_num == 3:
			dir = dirs["U"]
		else:
			assert False
		
		amnt = int(rgb[:5], 16)
		
		boundary += amnt
		
		curr = (curr[0] + amnt * dir[0], curr[1] + amnt * dir[1])
		path.append(curr)
	
	area = polygonArea(path)
	
	# picks theoreom
	res = area + (boundary//2) + 1
	return res


p1()
p2()
