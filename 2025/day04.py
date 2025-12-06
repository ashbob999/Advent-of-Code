# @formatter:off
from os.path import isfile, join as path_join
from sys import path as sys_path
sys_path.insert(1, path_join(sys_path[0], '..'))
file_name = path_join('input', 'day04.txt')
def to_list(mf=int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]
def to_gen(mf=int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)
def p1(*args): ans = part1(*args); print(ans); return ans
def p2(*args): ans = part2(*args); print(ans); return ans

if not isfile(file_name):
	from aoc import get_input_file
	get_input_file(session_path=['..', '.env'])
# @formatter:on

from utils import *

data = parsefile(file_name, "\n")


height = len(data)
width = len(data[0])


adj = [(x, y) for x in range(-1, 2) for y in range(-1, 2) if not(x==0 and y==0)]

def getrem(grid):
	rem = []
	
	for y in range(height):
		for x in range(width):
			if grid[y][x] != "@":
				continue
			
			ac = 0
			for dx, dy in adj:
				nx = x + dx
				ny = y + dy
				
				if nx >= 0 and nx < width:
					if ny >= 0 and ny < height:
						if grid[ny][nx] == "@":
							ac += 1
			
			if ac < 4:
				rem.append((x, y))
	
	return rem
				

def part1():
	return len(getrem(data))


def part2():
	tm = 0
	
	grid = [list(row) for row in data]

	while True:
		torem = getrem(grid)
		
		if len(torem) == 0:
			break
		
		tm += len(torem)
		
		for x, y in torem:
			grid[y][x] = "."
			
	return tm



p1()
p2()
