# @formatter:off
from os.path import isfile, join as path_join
from sys import path as sys_path
sys_path.insert(1, path_join(sys_path[0], '..'))
file_name = path_join('input', 'day07.txt')
def to_list(mf=int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]
def to_gen(mf=int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)
def p1(*args): ans = part1(*args); print(ans); return ans
def p2(*args): ans = part2(*args); print(ans); return ans

if not isfile(file_name):
	from aoc import get_input_file
	get_input_file(session_path=['..', '.env'])
# @formatter:on

from utils import *

data = parsefile(file_name, [[""], "\n"])

height = len(data)
width = len(data[0])

start = None

for y in range(height):
	for x in range(width):
		if data[y][x] == "S":
			start = (x, y)
			break
	if start is not None:
		break


def part1():
	s = 0
	
	ps = set([start])
	cp = set([start])
	
	while len(cp) > 0:
		next_p = set()
		
		for c in cp:
			if c[0] < 0 or c[0] >= width:
				continue
			if c[1] < 0 or c[1] >= height:
				continue
			
			nx = c[0]
			ny = c[1] +1
			
			if (nx, ny) in next_p:
				continue
				
			if (nx, ny) in ps:
				continue
			
			if ny >= height:
				continue
			
			if data[ny][nx] == "^":
				s += 1
				ps.add((nx-1, ny))
				ps.add((nx+1, ny))
				next_p.add((nx-1, ny))
				next_p.add((nx+1, ny))
			else:
				ps.add((nx, ny))
				next_p.add((nx, ny))
				
		cp = next_p

	
	return s

cache = {}
def count_time(op):
	cp = op
	
	if cp[0] < 0 or cp[0] > width:
		return 0
	if cp[1] < 0 or cp[1] > height:
		return 0
	
	
	if op in cache:
		return cache[op]

	while True:
		nx = cp[0]
		ny = cp[1] +1
		
		if ny >= height:
			cache[op] = 1
			return 1
			
		if data[ny][nx] == "^":
			# split
			for dx in [-1, +1]:
				nnx = nx + dx
				nny = ny
				
				pass
				
			res = count_time((nx-1, ny)) + count_time((nx+1, ny))
			cache[op] = res
			return res
	
		else:
			cp = (nx, ny)

		

def part2():
	return count_time(start)


p1()
p2()
