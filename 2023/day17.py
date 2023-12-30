# @formatter:off
from os.path import isfile, join as path_join
from sys import path as sys_path
sys_path.insert(1, path_join(sys_path[0], '..'))
file_name = path_join('input', 'day17.txt')
def to_list(mf: object = int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]
def to_gen(mf: object = int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)
def p1(*args): ans = part1(*args); print(ans); return ans
def p2(*args): ans = part2(*args); print(ans); return ans

if not isfile(file_name):
	from aoc import get_input_file
	get_input_file(session_path=['..', '.env'])
# @formatter:on

from utils import *

data = parsefile(file_name, [[int, ""], "\n"])

input = """2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533"""
data = parse(input, [[int, ""], "\n"])

height = len(data)
width = len(data[0])

def neb(x, y):
	r = []
	if x > 0:
		r.append((x-1, y))
		
	if x < width -1:
		r.append((x+1, y))
		
	if y > 0:
		r.append((x, y-1))
		
	if y < height-1:
		r.append((x, y+1))
		
	return r

def make_path(prev, start, end):
	if start == end:
		return []
	if end not in prev:
		return []
	
	path = []
	while end is not None:
		path.append(end)
		end = prev[end]
		
	return path[::-1]

def count_prev(prev, curr, new):
	# check last 4 for same axis
	n = 5
	last_n = [new]
	
	for i in range(n-1):
		if curr is None:
			break
		last_n.append(curr)
		curr = prev[curr]
		
	"""
	while curr is not None:
		last_4.append(curr)
		curr = prev[curr]
	"""
	
	print(last_n)
	
	if len(last_n) != n:
		return True
		
	# y axis
	if len(set(map(lambda v: v[1], last_n))) == 1:
		return False
		
	# x axis
	if len(set(map(lambda v: v[0], last_n))) == 1:
		return False
	
	return True

from collections import deque
import heapq

def search(grid, start, end):
	if start == end:
		return []
		
	to_check = []
	seen = set()
	dist = {}
	prev = {}
	
	prev[start] = None
	dist[start] = 0
	
	heapq.heappush(to_check, (0, start))
	
	while len(to_check) > 0:
		g, curr = heapq.heappop(to_check)
		seen.add(curr)
		
		if curr == end:
			return make_path(prev, start, end)
		
		for n in neb(*curr):
			if not count_prev(prev, curr, n):
				continue
			
			if n not in seen or True:
				w = grid[n[1]][n[0]]
				f = g + w
				if n not in dist or f < dist[n]:
					dist[n] = f
					prev[n] = curr
					heapq.heappush(to_check, (f, n))
					
	return make_path(prev, start, end)


def count_prev2(path, new):
	# check last 4 for same axis
	n = 5
	last_n = path[-(n-1):] + [new]
	
	#print(last_n)
	
	if len(last_n) != n:
		#print(path, last_n)
		return True
	
	#print(last_n)
	# y axis
	if len(set(map(lambda v: v[1], last_n))) == 1:
		return False
		
	# x axis
	if len(set(map(lambda v: v[0], last_n))) == 1:
		return False
	
	return True


def adj_pos(path):
	if len(path) == 0:
		assert False
	
	n = neb(*path[-1])
	if len(path) > 1:
		n = [v for v in n if v != path[-2]]
	
	n = [v for v in n if count_prev2(path, v)]
	
	return n

def dist(p1, p2):
	return abs(p1[0]-p2[0]) + abs(p1[1]-p2[1])

def search2(grid, start, end):
	if start == end:
		return []
		
	to_check = []
	seen = set()
	
	path = [start]
	
	mem = {}
	
	found = None
	
	heapq.heappush(to_check, (0, path))
	
	while len(to_check) > 0:
		g, curr = heapq.heappop(to_check)
		seen.add(tuple(curr))
		
		#print(curr[-1], g)
		if curr[-1] == end:
			print("match", g)
			if found is not None:
				if found[0] > g:
					found = (g, curr)
			else:
				found = (g, curr)
			continue
			
		if found is not None:
			if g >= found[0]:
				break
		
		for n in adj_pos(curr):
			w = grid[n[1]][n[0]]
			f = g + w
			if (curr[-1], n) not in mem or mem[(curr[-1], n)] > f:
			#if n not in dist or f < dist[n]:
				#dist[n] = f
				#prev[n] = curr
				#mem[(curr[-1], n)] = f
				heapq.heappush(to_check, (f, curr + [n]))
	
	if found is None:
		assert False
	return found[1]
	assert False


def part1():
	path = search2(data, (0, 0), (width-1, height-1))
	print(path)
	
	grid = [["." for x in range(width)] for y in range(height)]
	
	print()
	for p in path:
		grid[p[1]][p[0]] = "#"
	for l in grid:
		print("".join(l))
	print()
	
	s = 0
	for p in path[1:]:
		s += data[p[1]][p[0]]
		
	return s


def part2():
	pass


p1()
p2()
