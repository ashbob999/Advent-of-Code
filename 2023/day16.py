# @formatter:off
from os.path import isfile, join as path_join
from sys import path as sys_path
sys_path.insert(1, path_join(sys_path[0], '..'))
file_name = path_join('input', 'day16.txt')
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

def move(x, y, dir):
	if dir == 0:
		return x, y-1
	elif dir == 1:
		return x+1, y
	elif dir == 2:
		return x, y+1
	elif dir == 3:
		return x-1, y
	assert False

def beams(grid, markers, x, y, dir):
	"""
	0 up
	1 right
	2 down
	3 left
	"""
	
	while True:
		if x < 0 or x >= width:
			break
		if y < 0 or y >= height:
			break
		
		if markers[y][x][0] and dir in markers[y][x][1]:
			return
			
		markers[y][x][0] = True
		markers[y][x][1].add(dir)
		
		c = grid[y][x]
		if c == ".":
			#grid[y][x] == "#"
			x, y = move(x, y, dir)
			continue
		if dir % 2 == 0 and c == "|":
			x, y = move(x, y, dir)
			continue
		if dir % 2 == 1 and c == "-":
			x, y = move(x, y, dir)
			continue
		
		# vert split to hor
		if dir % 2 == 0 and c == "-":
			beams(grid, markers, x-1, y, 3)
			beams(grid, markers, x+1, y, 1)
			return
			
		# hor split to vert
		if dir % 2 == 1 and c == "|":
			beams(grid, markers, x, y-1, 0)
			beams(grid, markers, x, y+1, 2)
			return
			
		# up left
		if dir == 0 and c == "\\":
			x, y = x-1, y
			dir = 3
			continue
		
		# up right
		if dir == 0 and c == "/":
			x, y = x+1, y
			dir = 1
			continue
		
		# down left
		if dir == 2 and c == "/":
			x, y = x-1, y
			dir = 3
			continue
		
		# down right
		if dir == 2 and c == "\\":
			x, y = x+1, y
			dir = 1
			continue
			
		# left up
		if dir == 3 and c == "\\":
			x, y = x, y-1
			dir = 0
			continue
		
		# left down
		if dir == 3 and c == "/":
			x, y = x, y+1
			dir = 2
			continue
		
		# right up
		if dir == 1 and c == "/":
			x, y = x, y-1
			dir = 0
			continue
		
		# right down
		if dir == 1 and c == "\\":
			x, y = x, y+1
			dir = 2
			continue
		
		print(x, y, dir, c)
		assert False

def do_beams(x, y, dir):
	grid = [r[:] for r in data]
	markers = [[[False, set()] for x in range(width)] for y in range(height)]
	
	beams(grid, markers, x, y, dir)
	
	c = 0
	
	for y in range(height):
		for x in range(width):
			if markers[y][x][0]:
				c += 1
	
	return c


def part1():
	return do_beams(0, 0, 1)


def part2():
	maxv = 0
	
	# left
	for y in range(height):
		r = do_beams(0, y, 1)
		maxv = max(maxv, r)
	
	# right
	for y in range(height):
		r = do_beams(width-1, y, 3)
		maxv = max(maxv, r)
	
	# top
	for x in range(width):
		r = do_beams(x, 0, 2)
		maxv = max(maxv, r)
	
	# bottom
	for x in range(width):
		r = do_beams(x, height-1, 0)
		maxv = max(maxv, r)
	
	return maxv
	


p1()
p2()
