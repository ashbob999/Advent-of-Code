# @formatter:off
from os.path import isfile, join as path_join
from sys import path as sys_path
sys_path.insert(1, path_join(sys_path[0], '..'))
file_name = path_join('input', 'day10.txt')
def to_list(mf: object = int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]
def to_gen(mf: object = int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)
def p1(*args): ans = part1(*args); print(ans); return ans
def p2(*args): ans = part2(*args); print(ans); return ans

if not isfile(file_name):
	from aoc import get_input_file
	get_input_file(session_path=['..', '.env'])
# @formatter:on

from utils import *

data = parsefile(file_name,  ["\n"])

width = len(data[0])
height = len(data)
#print("grid", width, height, width*height)

start = None
for x in range(width):
	for y in range(height):
		if data[y][x] == "S":
			start = (x, y)
			break
	if start is not None:
		break

deltas = {
	"|": ((0, -1), (0, 1)),
	"-": ((-1, 0), (1, 0)),
	"L": ((0, -1), (1, 0)),
	"J": ((0, -1), (-1, 0)),
	"7": ((-1, 0), (0, 1)),
	"F": ((1, 0), (0, 1))
}


def next_pos(curr, prev):
	#print(curr, prev)
	delta = (prev[0]-curr[0], prev[1]-curr[1])
	#print(data[curr[1]][curr[0]])
	adj = list(deltas[data[curr[1]][curr[0]]])
	if delta not in adj:
		assert "delta not in adj"
	
	#print(adj, delta)
	adj.remove(delta)
	#print(adj, (curr[0]+adj[0][0], curr[1]+adj[0][1]))
	return (curr[0]+adj[0][0], curr[1]+adj[0][1])

loop = None

def part1():
	global loop
	loop = [start]
	
	pos = start
	
	if data[pos[1]-1][pos[0]+0] in ("|", "7", "F"):
		pos = (start[0], start[1]-1)
	elif data[pos[1]+1][pos[0]+0] in ("|", "L", "J"):
		pos = (start[0], start[1]+1)
	elif data[pos[1]+0][pos[0]-1] in ("-", "L", "F"):
		pos = (start[0]-1, start[1])
	elif data[pos[1]+0][pos[0]+1] in ("-", "J", "7"):
		pos = (start[0]+1, start[1])
	else:
		assert "no start"
	
	loop.append(pos)
	
	while pos != start:
		pos = next_pos(loop[-1], loop[-2])
		loop.append(pos)

	assert len(loop) % 2 == 1
	return len(loop) // 2


def bfs(start):
	to_check = [start]
	seen = set()
	
	while len(to_check) > 0:
		#print(len(to_check), len(seen))
		#print(to_check)
		curr = to_check[0]
		to_check.pop(0)
		
		if curr in seen:
			continue
		seen.add(curr)
		
		for adj in ((0, -1), (0, 1), (-1, 0), (1, 0)):
			np = (curr[0]+adj[0], curr[1]+adj[1])
			if 0 <= np[0] < width and 0 <= np[1] < height:
				if np not in loop:
					if np not in seen and np not in to_check:
						to_check.append(np)

	return seen


# https://en.m.wikipedia.org/wiki/Even%E2%80%93odd_rule
def is_point_in_path(x: int, y: int, poly) -> bool:
    """Determine if the point is on the path, corner, or boundary of the polygon

    Args:
      x -- The x coordinates of point.
      y -- The y coordinates of point.
      poly -- a list of tuples [(x, y), (x, y), ...]

    Returns:
      True if the point is in the path or is a corner or on the boundary"""
    num = len(poly)
    j = num - 1
    c = False
    for i in range(num):
        if (x == poly[i][0]) and (y == poly[i][1]):
            # point is a corner
            return True
        if (poly[i][1] > y) != (poly[j][1] > y):
            slope = (x - poly[i][0]) * (poly[j][1] - poly[i][1]) - (
                poly[j][0] - poly[i][0]
            ) * (y - poly[i][1])
            if slope == 0:
                # point is on boundary
                return True
            if (slope < 0) != (poly[j][1] < poly[i][1]):
                c = not c
        j = i
    return c



def check_group(group):
	# check touching edges
	for pos in group:
		if pos[0] == 0 or pos[0] == width-1:
			return False
		if pos[1] == 0 or pos[1] == height-1:
			return False
	
	# group is now surrounded by loop
	
	test_p = list(group)[0]
	
	return is_point_in_path(*test_p, loop)


def part2():
	points = set()
	
	groups = []
	seen = set()
	for x in range(width):
		for y in range(height):
			#print(x, y)
			if (x, y) not in seen and (x, y) not in loop:
				group = bfs((x, y))
				groups.append(group)
				seen |= set(group)
				#print(x, y, len(group))
				
	for g in groups:
		if check_group(g):
			points |= g
	
	return len(points)

p1()
p2()
