# @formatter:off
from os.path import isfile, join as path_join
from sys import path as sys_path
sys_path.insert(1, path_join(sys_path[0], '..'))
file_name = path_join('input', 'day23.txt')
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

height = len(data)
width = len(data[0])

start = None
for x in range(width):
	if data[0][x] == ".":
		start = (x, 0)
		break
		
emd = None
for x in range(width):
	if data[height-1][x] == ".":
		end = (x, height-1)
		break

adj = ((0, 1), (0, -1), (1, 0), (-1, 0))

def valid(x, y):
	if 0 <= x < width and 0 <= y < height:
		if data[y][x] != "#":
			return True
	return False

def next(pos):
	n = []
	for a in adj:
		nx = pos[0] + a[0]
		ny = pos[1] + a[1]
		if valid(nx, ny):
			n.append((nx, ny))
				
	return n

def longest(path, curr, end, has_slopes):
	
	dist = 0
	
	n = [curr]
	
	while True:
		if len(n) == 0:
			return 0
		elif len(n) == 1:
			curr = n[0]
			dist += 1
			
			if has_slopes:
				cp = data[curr[1]][curr[0]]
				if cp == ">":
					path.add(curr)
					curr = (curr[0]+1, curr[1])
					dist += 1
				elif cp == "<":
					path.add(curr)
					curr = (curr[0]-1, curr[1])
					dist += 1
				elif cp == "v":
					path.add(curr)
					curr = (curr[0], curr[1]+1)
					dist += 1
				elif cp == "^":
					path.add(curr)
					curr = (curr[0], curr[1]-1)
					dist += 1
		
			if not valid(*curr):
				return 0
			if curr in path:
				return 0
				
			path.add(curr)
				
			if curr == end:
				return dist
				
		else:
			max_dist = 0
			
			for np in n:
				path_ = path.copy()
				d = longest(path_, np, end, has_slopes)
				if d > max_dist:
					max_dist = d
			
			return dist + max_dist
		
		n = next(curr)
		n = [v for v in n if v not in path]
	
	return dist

def part1():
	d = longest(set(), start, end, True)
	return d - 1

def bfs(path, curr, ends):
	dist = 0
	
	n = [curr]
	while True:
		if len(n) == 0:
			return None
		elif len(n) == 1:
			
				
			curr = n[0]
			dist += 1
			path.add(curr)
			
			if curr in ends:
				return curr, dist
		else:
			return None
		
		n = next(curr)
		n = [v for v in n if v not in path]
	

def get_nodes(start, end):
	# list of nodes
	nodes = []
	
	for y in range(height):
		for x in range(width):
			if valid(x, y):
				n = next((x, y))
				if len(n) > 2:
					nodes.append((x, y))
	
	nodes.append(start)
	nodes.append(end)

	paths = {}
	for i in range(len(nodes)):
		node = nodes[i]
		n = next(node)
		for v in n:
			path = set([node, v])
			r = bfs(path, v, nodes)
			if r is not None:
				p1 = node
				p2 = r[0]
				
				if p1 in paths and p2 in paths[p1]:
					assert paths[p1][p2] == r[1]
				if p2 in paths and p1 in paths[p2]:
					assert paths[p2][p1] == r[1]
					
				if p1 not in paths:
					paths[p1] = {}
				if p2 not in paths:
					paths[p2] = {}
				
				paths[p1][p2] = r[1]
				paths[p2][p1] = r[1]
				
	return paths

paths = get_nodes(start, end)


def longest2(path, start, end, paths):
	dist = 0
	
	if start == end:
		return 0
	
	max_dist = 0
	for np, dist in paths[start].items():
		if np not in path:
			r = longest2(path | set([np]), np, end, paths)
			d = dist + r
			if d > max_dist:
				max_dist = d
	
	return max_dist

def part2():
	d = longest2(set([start]), start, end, paths)
	return d


p1()
p2()
