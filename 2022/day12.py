# @formatter:off
from os.path import isfile, join as path_join
from sys import path as sys_path
sys_path.insert(1, path_join(sys_path[0], '..'))
file_name = path_join('input', 'day12.txt')
def to_list(mf: object = int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]
def to_gen(mf: object = int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)
def p1(*args): ans = part1(*args); print(ans); return ans
def p2(*args): ans = part2(*args); print(ans); return ans

if not isfile(file_name):
	from aoc import get_input_file
	get_input_file(session_path=['..', '.env'])
# @formatter:on

from utils import parsefile, parse

grid = parsefile(file_name, [list, "\n"])

rd = """Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi"""
grida = parse(rd, [list, "\n"])

width = len(grid[0])
height = len(grid)
print(width, height)

start = None
end = None

for x in range(width):
	for y in range(height):
		if grid[y][x] == "S":
			start = (x, y)
		if grid[y][x] == "E":
			end = (x, y)

heights = {chr(i + ord("a")): i for i in range(26)}
heights["S"] = 0
heights["E"] = 25
print(heights)

def bfs(grid, start, end):
	visited = set()
	dists = {}
	dists[start] = 0
	
	to_visit = [(start, 0)]
	
	while len(to_visit) > 0:
		#print(len(to_visit))
		curr, curr_dist = to_visit[0]
		#to_visit.remove((curr, curr_dist))
		to_visit.pop(0)
		
		if curr == end:
			return curr_dist
		
		if curr in visited:
			continue
			
		visited.add(curr)
		#curr_dist = dists[curr]
		
		next_p = []
		
		xp = curr[0]
		yp = curr[1]
		
		curr_height = heights[grid[yp][xp]]
		
		for y in [-1, 1]:
			if 0 <= yp+y < height:
				nh = heights[grid[yp+y][xp]]
				if nh <= curr_height + 1:
					next_p.append((xp, yp+y))

		for x in [-1, 1]:
			if 0 <= xp+x < width:
				nh = heights[grid[yp][xp+x]]
				if nh <= curr_height + 1:
					next_p.append((xp+x, yp))
			
		#print(curr, next_p)
			
		for np in next_p:
			if np == end:
				print(end, curr_dist+1)
				#return curr_dist + 1
			#to_visit.add((np, curr_dist+1))
			#continue
			if np in visited:
				continue
				if curr_dist +1 < dists[np]:
					to_visit.append(np)
					dists[np] = curr_dist +1
					#print("seen lower", np)
			else:
				to_visit.append((np, curr_dist+1))
				dists[np] = curr_dist +1
			#print("not seen", np)

	#return dists[end]
	return 10000000000

def part1():
	dist = bfs(grid, start, end)
	return dist


def part2():
	min_dist = bfs(grid, start, end)
	
	for y in range(height):
		for x in range(width):
			if grid[y][x] == "a":
				dist = bfs(grid, (x, y), end)
				min_dist = min(min_dist, dist)
			
	return min_dist


p1()
p2()
