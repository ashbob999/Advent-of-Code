# @formatter:off
from os.path import isfile, join as path_join
from sys import path as sys_path
sys_path.insert(1, path_join(sys_path[0], '..'))
file_name = path_join('input', 'day13.txt')
def to_list(mf: object = int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]
def to_gen(mf: object = int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)
def p1(*args): ans = part1(*args); print(ans); return ans
def p2(*args): ans = part2(*args); print(ans); return ans

if not isfile(file_name):
	from aoc import get_input_file
	get_input_file(session_path=['..', '.env'])
# @formatter:on

from utils import *

data = parsefile(file_name, [[list, "\n"], "\n\n"])


def find_h(grid, ex=None):
	# index, count
	res = (-1, -1)
	width = len(grid)
	
	for i in range(width-1):
		if grid[i] != grid[i+1]:
			continue
		if ex is not None and ex == i:
			continue
		matches = 0
		for j in range(1, i+1):
			if i-j < 0 or i+j+1 >= width:
				break
			if grid[i-j] != grid[i+j+1]:
				if i-j > 0 or i+j+1 < width-1:
					matches = -1
					break
				break
			matches += 1
		if (matches > res[1]):
			res = (i, matches)
		elif (matches == res[1]):
			if matches != -1:
				print("duplicate matches", res, matches)
				#assert False
	
	return res


def transpose(tile):
	return ["".join(x)[::-1] for x in zip(*tile)]


def find_v(grid, ex=None):
	# flip grid
	
	# transpose 90 deg clockwise
	grid2 = transpose(grid)
	
	return find_h(grid2, ex)


def find(grid, ex=None):
	if ex is not None:
		if ex[0] == 0:
			h = find_h(grid, ex[1])
			v = find_v(grid)
		else:
			h = find_h(grid)
			v = find_v(grid, ex[1])
	else:
		h = find_h(grid)
		v = find_v(grid)
	
	if h[0] == -1 and v[0] == -1:
		return (None, (None, None))
	
	if h[1] > v[1]:
		return (0, h)
	elif h[1] < v[1]:
		return (1, v)
	else:
		print("equal indexes", h, v)
		for l in grid:
			print("".join(l))
		assert False
	
	return (None, (-1, -1))

def part1():
	s = 0
	
	for grid in data:
		res = find(grid)
		if res[0] == 0:
			s += (res[1][0]+1) * 100
		elif res[0] == 1:
			s += res[1][0]+1
		else:
			print("no match", grid)
			assert False
	
	return s


def part2():
	s = 0
	
	for grid in data:
		p1_res = find(grid)
		r = None
		
		for y in range(len(grid)):
			for x in range(len(grid[0])):
				grid_ = [r[:] for r in grid]
				if grid_[y][x] == "#":
					grid_[y][x] = "."
				else:
					grid_[y][x] = "#"
					
				res = find(grid_, (p1_res[0], p1_res[1][0]))
				if res[0] is not None:
					r = res
					break
					
			if r is not None:
				break
		
		if r[0] == 0:
			s += (r[1][0]+1) * 100
		elif res[0] == 1:
			s += r[1][0]+1
		else:
			print("no match", grid)
			assert False
	
	return s


p1()
p2()
