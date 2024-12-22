# @formatter:off
from os.path import isfile, join as path_join
from sys import path as sys_path
sys_path.insert(1, path_join(sys_path[0], '..'))
file_name = path_join('input', 'day20.txt')
def to_list(mf=int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]
def to_gen(mf=int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)
def p1(*args): ans = part1(*args); print(ans); return ans
def p2(*args): ans = part2(*args); print(ans); return ans

if not isfile(file_name):
	from aoc import get_input_file
	get_input_file(session_path=['..', '.env'])
# @formatter:on

from utils import *

grid = parsefile(file_name,  [list, "\n"])

w = len(grid[0])
h = len(grid)

start = None
end = None

for y in range(h):
	for x in range(w):
		if grid[y][x] == "S":
			start = (x, y)
		elif grid[y][x] == "E":
			end = (x, y)

import heapq

adj =  ((0, 1), (0, -1), (1, 0), (-1, 0))

def dfs(s, e, grid):
	
	scores = {s: 0}
	
	to_check = [(0 ,s)]
	
	while len(to_check):
		score, curr = heapq.heappop(to_check)
		
		for dx, dy in adj:
			nx = curr[0] + dx
			ny = curr[1] + dy
			
			if nx >= 0 and nx < w and ny >=0 and ny < h and grid[ny][nx] != "#":
				ns = score + 1
				
				if (nx, ny) == e:
					return ns
				
				if (nx, ny) not in scores or ns < scores[(nx, ny)]:
					scores[(nx, ny)]=ns
					heapq.heappush(to_check,  (ns, (nx, ny)))

fastest = dfs(start, end, grid)
print(fastest)

from copy import deepcopy

def part1():
	c = 0
	print(w, h)


	for y in range(h):
		for x in range(w):
			if grid[y][x] == "#":
				adjc = 0
				for dx, dy in adj:
					nx = x + dx
					ny = y + dy
					if nx >=0 and nx <w and ny >=0 and ny < h and grid[ny][nx]!="#":
						adjc += 1
				
				if adjc >= 2:
					print(y, x)
					g = deepcopy(grid)
					g[y][x] = "."
						
					r = dfs(start, end, g)
					if r <= fastest -100:
						c +=1
	
	return c


def part2():
	pass


p1()
p2()
