from os.path import isfile, join as path_join
from sys import path as sys_path
sys_path.insert(1, path_join(sys_path[0], '..'))
file_name = path_join('input', 'day15.txt')
def to_list(mf: object = int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]
def to_gen(mf: object = int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)
def p1(*args): ans = part1(*args); print(ans); return ans
def p2(*args): ans = part2(*args); print(ans); return ans

if not isfile(file_name):
	from aoc import get_input_file
	get_input_file(session_path=['..', '.env'])

from utils import parsefile

grid = parsefile(file_name, [[int, ""], "\n"])

w = len(grid[0])
h = len(grid)

dir = [(0, 1), (0, -1), (1, 0), (-1, 0)]

from heapq import *

def hf(start):
	return abs(start[0]) + abs(start[1])

def create_path(came_from, current):
	tp = [current]
	while current in came_from:
		current = came_from[current]
		tp.append(current)
		
	return tp[::-1]

def a_star(start, end, grid):
	w = len(grid[0])
	h = len(grid)
	
	in_heap = set()
	heap = []
	heappush(heap, (0, start))
	in_heap.add(start)
	
	came_from = {}
	
	g_score = {start:0}
	
	f_score = {start:hf(start)}
	
	while len(heap) > 0:
		curr_dist, curr = heappop(heap)
		in_heap.remove(curr)
		
		if curr == end:
			return create_path(came_from, curr)
			
		for d in dir:
			nx = curr[0] + d[0]
			ny = curr[1] + d[1]
			
			if nx >= 0 and nx < w and ny >= 0 and ny < h:
				tg_score = g_score[curr] + grid[ny][nx]
				
				if (nx, ny) not in g_score or tg_score < g_score[(nx, ny)]:
					came_from[(nx, ny)] = curr
					
					g_score[(nx, ny)] = tg_score
					
					f_score[(nx, ny)] = tg_score + hf((nx, ny))
					
					if (nx, ny) not in in_heap:
						heappush(heap, (f_score[(nx, ny)], (nx, ny)))
						in_heap.add((nx, ny))

	return None

def part1():
	start = (0, 0)
	end = (w-1, h-1)
	
	res = a_star(start, end, grid)

	dist = 0
	if res is not None:
		for d in res:
			if d != start:
				dist += grid[d[1]][d[0]]

	return dist

def part2():
	large_grid = [[0 for x in range(w*5)] for y in range(h*5)]
	
	for ty in range(5):
		for tx in range(5):
			inc = ty + tx

			for y in range(h):
				for x in range(w):
					if grid[y][x] + inc > 9:
						nv = 1 + (grid[y][x] + inc) % 10
						large_grid[y+h*ty][x+w*tx] = nv
					else:
						large_grid[y+h*ty][x+w*tx] = grid[y][x] + inc
					
	start = (0, 0)
	end = (w*5-1, h*5-1)
	#end = (w, h)

	res = a_star(start, end, large_grid)

	dist = 0
	if res is not None:
		for d in res:
			if d != start:
				dist += large_grid[d[1]][d[0]]

	return dist


p1()
p2()
