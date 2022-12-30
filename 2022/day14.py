# @formatter:off
from os.path import isfile, join as path_join
from sys import path as sys_path
sys_path.insert(1, path_join(sys_path[0], '..'))
file_name = path_join('input', 'day14.txt')
def to_list(mf: object = int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]
def to_gen(mf: object = int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)
def p1(*args): ans = part1(*args); print(ans); return ans
def p2(*args): ans = part2(*args); print(ans); return ans

if not isfile(file_name):
	from aoc import get_input_file
	get_input_file(session_path=['..', '.env'])
# @formatter:on

from utils import parsefile, parse

lines = parsefile(file_name, [[[int, ","], "->"], "\n"])

cave = {}

minx = 10000000000
maxx = 0
maxy = 0

for line in lines:
	for i in range(len(line)-1):
		po1 = line[i]
		po2 = line[i+1]
		
		minx = min(minx, po1[0], po2[0])
		maxx = max(maxx, po1[0], po2[0])
		maxy = max(maxy, po1[1], po2[1])
		
		if po1[0]==po2[0]: # vertical
			yd = 1 if po1[1] <= po2[1] else -1
			for y in range(po1[1], po2[1]+yd, yd):
				cave[(po1[0], y)] = "#"
		elif po1[1] == po2[1]: # horizontal
			xd = 1 if po1[0] <= po2[0] else -1
			for x in range(po1[0], po2[0]+xd, xd):
				cave[(x, po1[1])] = "#"

def get_move(cave, drop, use_bounds=True):
	pos=drop
	did_move = True
	while did_move:
		did_move = False
		
		if use_bounds:
			if pos[0] < minx or pos[0] > maxx:
				return pos
		
		below = (pos[0], pos[1]+1)
		if below not in cave:
			pos = below
			did_move = True
			continue
			
		left = (pos[0]-1, pos[1]+1)
		if left not in cave:
			pos = left
			did_move = True
			continue
			
		right = (pos[0]+1, pos[1]+1)
		if right not in cave:
			pos = right
			did_move = True
			continue
			
		break
					
	return pos
		

def part1():
	cv = cave.copy()
	drop = (500, 0)
	
	i = 0
	while True:
		pos = get_move(cv, drop)
		if pos[0] < minx or pos[0] > maxx:
			break
		
		cv[pos] = "o"
		
		i += 1
		
	return i

def part2():
	bottom = maxy + 2
	cv = cave.copy()
	drop = (500, 0)
	
	for x in range(minx - 500, maxx+500):
		cv[(x, bottom)] = "#"
		
	i = 0
	while True:
		pos = get_move(cv, drop, False)
		if pos == drop:
			break
		
		cv[pos] = "o"
		
		i += 1
	
	return i+1


p1()
p2()
