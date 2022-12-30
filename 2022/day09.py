# @formatter:off
from os.path import isfile, join as path_join
from sys import path as sys_path
sys_path.insert(1, path_join(sys_path[0], '..'))
file_name = path_join('input', 'day09.txt')
def to_list(mf: object = int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]
def to_gen(mf: object = int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)
def p1(*args): ans = part1(*args); print(ans); return ans
def p2(*args): ans = part2(*args); print(ans); return ans

if not isfile(file_name):
	from aoc import get_input_file
	get_input_file(session_path=['..', '.env'])
# @formatter:on

from utils import parsefile

moves = parsefile(file_name, [[str, 1, int, " "], "\n"])

def diff(p1, p2):
	dx = abs(p1[0]-p2[0])
	dy = abs(p1[1]-p2[1])
	if dx==0 and dy==0:
		return 0 # on top, no move
	if dx == 1 and dy ==1:
		return 0 # diag, no move
	if (dx==0 and dy<=1) or (dy==0 and dx<=1):
		return 0 # same line, no move
	if (dx==0 and dy>1) or (dy==0 and dx>1):
		return 1 # same line, move
	return 2 # diag, 2x1, move
	

def part1():
	visited = set()
	
	start = (0, 0)
	head = start
	tail = start
	
	for dir, count in moves:
		for i in range(count):
			if dir == "L":
				head = (head[0]-1, head[1])
				d = diff(head, tail)
				if d == 1:
					tail = (tail[0]-1, tail[1])
				elif d == 2:
					tail = (tail[0]-1, head[1])
			elif dir == "R":
				head = (head[0]+1, head[1])
				d = diff(head, tail)
				if d == 1:
					tail = (tail[0]+1, tail[1])
				elif d == 2:
					tail = (tail[0]+1, head[1])
			elif dir == "U":
				head = (head[0], head[1]-1)
				d = diff(head, tail)
				if d == 1:
					tail = (tail[0], tail[1]-1)
				elif d == 2:
					tail = (head[0], tail[1]-1)
			elif dir == "D":
				head = (head[0], head[1]+1)
				d = diff(head, tail)
				if d == 1:
					tail = (tail[0], tail[1]+1)
				elif d == 2:
					tail = (head[0], tail[1]+1)
			
			visited.add(tail)
			
	return len(visited)
	

def cm(p1, p2):
	dx = abs(p1[0]-p2[0])
	dy = abs(p1[1]-p2[1])
	xd = -1 if p1[0]<p2[0] else 1
	yd = -1 if p1[1]<p2[1] else 1
	if dx == 0 and dy==0:
		return (0, 0)
	if dx==1 and dy==1:
		return (0, 0)
	if (dx==0 and dy==1) or (dx==1 and dy==0):
		return (0, 0)
	if (dx==0 and dy==2):
		return (0, yd)
	if (dx==2 and dy==0):
		return (xd, 0)
	if dx+dy >=3:
		return (xd, yd)
	
	print("unkniwn", p1, p2)
	return None
	

def part2():
	visited = set()
	
	start = (0, 0)
	knots = [start] * 10
	
	for dir, count in moves:
		for i in range(count):
			if dir == "L":
				knots[0] = (knots[0][0]-1, knots[0][1])
				for i in range(1, 10):
					d = cm(knots[i-1], knots[i])
					knots[i] = (knots[i][0]+d[0], knots[i][1]+d[1])
			elif dir == "R":
				knots[0] = (knots[0][0]+1, knots[0][1])
				for i in range(1, 10):
					d = cm(knots[i-1], knots[i])
					knots[i] = (knots[i][0]+d[0], knots[i][1]+d[1])
			elif dir == "U":
				knots[0] = (knots[0][0], knots[0][1]-1)
				for i in range(1, 10):
					d = cm(knots[i-1], knots[i])
					knots[i] = (knots[i][0]+d[0], knots[i][1]+d[1])
			elif dir == "D":
				knots[0] = (knots[0][0], knots[0][1]+1)
				for i in range(1, 10):
					d = cm(knots[i-1], knots[i])
					knots[i] = (knots[i][0]+d[0], knots[i][1]+d[1])
			
			visited.add(knots[-1])
			
	return len(visited)


p1()
p2()
