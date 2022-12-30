# @formatter:off
from os.path import isfile, join as path_join
from sys import path as sys_path
sys_path.insert(1, path_join(sys_path[0], '..'))
file_name = path_join('input', 'day24.txt')
def to_list(mf: object = int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]
def to_gen(mf: object = int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)
def p1(*args): ans = part1(*args); print(ans); return ans
def p2(*args): ans = part2(*args); print(ans); return ans

if not isfile(file_name):
	from aoc import get_input_file
	get_input_file(session_path=['..', '.env'])
# @formatter:on

from utils import parsefile, parse

import sys
sys.setrecursionlimit(100000)

data = parsefile(file_name, [str, "\n"])
rd = """#.######
#>>.<^<#
#.<..<<#
#>v.><>#
#<^v^^>#
######.#"""
dataa = parse(rd, [str, "\n"])

width = len(data[0])
height = len(data)

start = [0, 0]
while data[start[1]][start[0]] != ".":
	start[0] += 1

end = [0, height-1]
while data[end[1]][end[0]] != ".":
	end[0] += 1
	
from copy import deepcopy

empty = [[list() for x in range(width)] for y in range(height)]
grid = deepcopy(empty)

pos = set()
edges = set()

for y in range(height):
	for x in range(width):
		if data[y][x] == "#":
			grid[y][x].append("#")
			empty[y][x].append("#")
			edges.add((x, y))
		elif data[y][x] == ".":
			pass#grid[y][x] = []
		else:
			grid[y][x] = [data[y][x]]
			pos.add((x, y))
		
#for r in grid:
#	print(r)
	
print(start, end)

grid_steps = [pos]
#print(pos)

grid_temp = deepcopy(grid)
for i in range(2000):
	if i%100 ==0:print("i", i)
	g = deepcopy(empty)
	positions = set()
	for y in range(1, height-1):
		for x in range(1, width-1):
			for bliz in grid_temp[y][x]:
				np = [x, y]
				if bliz == "^":
					np[1] -= 1
					if np[1] <= 0:
						np[1] = height-2
				elif bliz == "v":
					np[1] += 1
					if np[1] >= height-1:
						np[1] = 1
				elif bliz == "<":
					np[0] -= 1
					if np[0] <= 0:
						np[0] = width-2
				elif bliz == ">":
					np[0] += 1
					if np[0] >= width-1:
						np[0] = 1
				
				g[np[1]][np[0]].append(bliz)
				positions.add(tuple(np))
				
	grid_steps.append(positions)
	grid_temp = g

dirs = [(1, 0), (0, 1), (-1, 0), (-1, 0)]

endp = []

def bfs(start, end):
	start = tuple(start)
	end = tuple(end)
	
	seen = set()
	#to_check = set()
	#to_check.add((start, 0))
	to_check = [(start, 0)]
	
	while len(to_check) > 0:
		#curr, steps = list(to_check)[0]
		#to_check.remove((curr, steps))
		curr, steps = to_check[0]
		to_check.pop(0)
		
		if (curr, steps) in seen:
			continue
		
		seen.add((curr, steps))
		
		g = grid_steps[steps]
		
		# wait
		if (curr[1], curr[0]) not in g:
			to_check.append((curr, steps+1))
			
		# move
		for dir in dirs:
			np = (curr[0]+dir[0], curr[1]+dir[1])
			if 0 <= np[0] < width and 0 <= np[1] < height:
				if (np[1], np[0]) not in g and (np[0], np[1]) not in edges:
					if np == end:
						#print("end", steps+1)
						#global endp
						#endp.append(steps+1)
						#print("min", min(endp))
						return steps+1
					else:
						to_check.append((np, steps+1))
	
	
def part1():
	print("starting")
	return bfs(start, end)


def part2():
	pass


p1() # > 149
p2()
