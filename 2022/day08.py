# @formatter:off
from os.path import isfile, join as path_join
from sys import path as sys_path
sys_path.insert(1, path_join(sys_path[0], '..'))
file_name = path_join('input', 'day08.txt')
def to_list(mf: object = int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]
def to_gen(mf: object = int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)
def p1(*args): ans = part1(*args); print(ans); return ans
def p2(*args): ans = part2(*args); print(ans); return ans

if not isfile(file_name):
	from aoc import get_input_file
	get_input_file(session_path=['..', '.env'])
# @formatter:on

from utils import parsefile

grid = parsefile(file_name, [[int, ""], "\n"])

visible = set()

def part1():
	global visible
	
	for x in range(len(grid[0])):
		visible.add((x, 0))
		visible.add((x, len(grid)-1))
		
	for y in range(len(grid)):
		visible.add((0, y))
		visible.add((len(grid[0])-1, y))
	
	# hor
	for y in range(1, len(grid)-1):
		cm = grid[y][0]
		for x in range(1, len(grid[0])-1):
			if grid[y][x] > cm:
				visible.add((x, y))
				cm = grid[y][x]

		cm = grid[y][-1]
		for x in range(len(grid[0])-2, 0, -1):
			if grid[y][x] > cm:
				visible.add((x, y))
				cm = grid[y][x]
				
	for x in range(1, len(grid[0])-1):
		cm = grid[0][x]
		for y in range(1, len(grid)-1):
			if grid[y][x] > cm:
				visible.add((x, y))
				cm = grid[y][x]
		
		cm = grid[-1][x]
		for y in range(len(grid)-2, 0, -1):
			if grid[y][x] > cm:
				visible.add((x, y))
				cm = grid[y][x]

	return len(visible)

def score(pos):
	xp = pos[0]
	yp = pos[1]
	cp = grid[yp][xp]
	
	right =0
	cm = grid[yp][xp]
	for x in range(xp+1, len(grid[0])):
		right +=1
		if grid[yp][x] >= cp:
			break
		
	left =0
	cm = grid[yp][xp]
	for x in range(xp-1, -1, -1):
		left+=1
		if grid[yp][x] >= cp:
			break
			
	# l to r
	down=0
	cm = grid[yp][xp]
	for y in range(yp+1, len(grid)):
		down+=1
		if grid[y][xp] >= cp:
			break
	
	up=0
	cm = grid[yp][xp]
	for y in range(yp-1, -1, -1):
		up+=1
		if grid[y][xp] >= cp:
			break

	return left * right * up * down

def part2():
	return max(map(score, visible))


p1()
p2()
