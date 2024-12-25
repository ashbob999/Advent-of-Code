# @formatter:off
from os.path import isfile, join as path_join
from sys import path as sys_path
sys_path.insert(1, path_join(sys_path[0], '..'))
file_name = path_join('input', 'day25.txt')
def to_list(mf=int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]
def to_gen(mf=int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)
def p1(*args): ans = part1(*args); print(ans); return ans
def p2(*args): ans = part2(*args); print(ans); return ans

if not isfile(file_name):
	from aoc import get_input_file
	get_input_file(session_path=['..', '.env'])
# @formatter:on

from utils import *

grids = parsefile(file_name, [["\n"], "\n\n"])

keys = []
locks = []

max_h = 7

for g in grids:
	type = None
	if "." in g[0]:
		type = 1 # key
	elif "." in g[-1]:
		type = 0 # lock
		
	heights = [0] * len(g[0])
	
	for x in range(len(heights)):
		h = [g[y][x] for y in range(max_h)].count("#")
		heights[x] = h
		
	if type == 0:
		locks.append(heights)
	elif type == 1:
		keys.append(heights)

def part1():
	t = 0
	
	for lock in locks:
		for key in keys:
			r = [lock[i] + key[i] for i in range(len(lock))]
			
			if all([v <= max_h for v in r]):
				t += 1
	
	return t


def part2():
	pass


p1()
p2()
