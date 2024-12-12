# @formatter:off
from os.path import isfile, join as path_join
from sys import path as sys_path
sys_path.insert(1, path_join(sys_path[0], '..'))
file_name = path_join('input', 'day12.txt')
def to_list(mf=int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]
def to_gen(mf=int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)
def p1(*args): ans = part1(*args); print(ans); return ans
def p2(*args): ans = part2(*args); print(ans); return ans

if not isfile(file_name):
	from aoc import get_input_file
	get_input_file(session_path=['..', '.env'])
# @formatter:on

from utils import *

data = parsefile(file_name,  [str, "\n"])

w = len(data[0])
h = len(data)

def bfs(start):
	
	seen = set()
	group = set([start])
	
	v = data[start[1]][start[0]]
	
	
	to_check = [start]
	
	while len(to_check):
		curr = to_check.pop(0)
		
		if curr in seen:
			continue
			
		seen.add(curr)
		
		for dx in (-1, 1):
			nx = curr[0] + dx
			if nx >= 0 and nx < w:
				if data[curr[1]][nx] == v:
					group.add((nx, curr[1]))
					to_check.append((nx, curr[1]))
					
		for dy in (-1, 1):
			ny = curr[1] + dy
			if ny >= 0 and ny < h:
				if data[ny][curr[0]] == v:
					group.add((curr[0], ny))
					to_check.append((curr[0], ny))
	
	return group

def find_regions():
	seen = set()

	regions = []

	for y in range(h):
		for x in range(w):
			if (x, y) in seen:
				continue
			
			r = bfs((x, y))
			regions.append(r)
			for v in r:
				seen.add(v)
				
	return regions


regions = find_regions()


def part1():
	t = 0
	
	for r in regions:
		a = len(r)
		p = 0
		
		val = None
		for v in r:
			if val is None:
				val = data[v[1]][v[0]]
				
			for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
				nx = v[0] + dx
				ny = v[1] + dy
				
				if nx < 0 or nx >= w or ny < 0 or ny >= h or data[ny][nx] != val:
					p+= 1
		
		t += a * p
		
	return t
				
def sides(r):
	s = 0
	
	perim = set()
	
	val = None
	c = 0
	for v in r:
		if val is None:
			val = data[v[1]][v[0]]
		

		inv = 0
		diffs = []
		for dx in (-1, 1):
			for dy in (-1, 1):
				if (v[0], v[1] + dy) not in r and (v[0] + dx, v[1]) not in r:
					s += 1
				elif (v[0], v[1] + dy) in r and (v[0] + dx, v[1]) in r and (v[0] + dx, v[1] + dy) not in r:
					s += 1
		"""
			if nx < 0 or nx >= w or ny < 0 or ny >= h or data[ny][nx] != val:
				inv += 1
				diffs.append((dx, dy))
				perim.add((nx, ny))
		"""
		"""
		if inv == 4:
			#c += 4
			s += 4
		elif inv == 3:
			#c += 2
			s += 2
		elif inv == 2:
			assert len(diffs) == 2
			dx = abs(diffs[0][0]) + abs(diffs[1][0])
			dy = abs(diffs[0][1]) + abs(diffs[1][1])
			#print(diffs, dx, dy)
			if dx != 0 and dy != 0:
				#c += 1
				s += 1
		print("v", v, inv)
		if inv == 1:
			pass
		"""
	
	print("mid", s)
	
	"""
	for v in perim:
		inv = 0
		diffs=[]
		for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
			nx = v[0] + dx
			ny = v[1] + dy
			
			#if nx >=0 and nx < w and ny >= 0 and ny < h and data[ny][nx] == val:
			if (nx, ny) in r:
				inv += 1
				diffs.append((dx, dy))
				#perim.add((nx, ny))
		print("inv", inv)
		if inv == 1:
			pass
		elif inv == 2:
			assert len(diffs) == 2
			dx = abs(diffs[0][0]) + abs(diffs[1][0])
			dy = abs(diffs[0][1]) + abs(diffs[1][1])
			#print(diffs, dx, dy)
			if dx != 0 and dy != 0:
				#c += 3
				#s += 1
				print(v, diffs)
				
				cx = diffs[0][0] + diffs[1][0]
				cy = diffs[0][1] + diffs[1][1]
				tx = v[0] + cx
				ty = v[1] + cy
				print(cx, cy, tx, ty, (tx, ty) in r)
				if (tx, ty) in r:
					s += 1
		elif inv == 3:
			#c += 6
			s+=2
		elif inv == 4:
			#c += 12
			s+=4
	"""
	
	#s = c // 2 + 2
	print(r, s, c)
	print()
	assert(s >= 4)
	assert(s %2 == 0)
	return s


def part2():
	t = 0
	
	for r in regions:
		a = len(r)
		s = sides(r)
		print(a, s)
		t += a * s
		
	return t

# si / 180 + 2

p1()
p2() # != 956051, < 887702, < 886714

# != 882931