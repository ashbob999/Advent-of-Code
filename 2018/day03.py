# @formatter:off
from os.path import isfile, join as path_join
from sys import path as sys_path
sys_path.insert(1, path_join(sys_path[0], '..'))
file_name = path_join('input', 'day03.txt')
def to_list(mf=int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]
def to_gen(mf=int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)
def p1(*args): ans = part1(*args); print(ans); return ans
def p2(*args): ans = part2(*args); print(ans); return ans

if not isfile(file_name):
	from aoc import get_input_file
	get_input_file(session_path=['..', '.env'])
# @formatter:on

from utils import *

data = parsefile(file_name, "\n")

rects = []
for d in data:
	s = d.split(" ")
	id = int(s[0][1:])
	x = int(s[2].split(",")[0])
	y = int(s[2].split(",")[1][:-1])
	
	w = int(s[3].split("x")[0])
	h = int(s[3].split("x")[1])
	
	rect = (id, (x, y),(w, h))
	rects.append(rect)

g = {}

def part1():
	global g
	
	for r in rects:
		for y in range(r[1][1], r[1][1] + r[2][1]):
			for x in range(r[1][0], r[1][0] + r[2][0]):
				if (x, y) not in g:
					g[(x, y)] = 1
				else:
					g[(x, y)] += 1
				
	return sum(1 for k, v in g.items() if v >= 2)


def part2():
	for r in rects:
		overlap = False
		for y in range(r[1][1], r[1][1] + r[2][1]):
			for x in range(r[1][0], r[1][0] + r[2][0]):
				if g[(x, y)] > 1:
					overlap = True
					break
					
			if overlap:
				break
				
		if not overlap:
			return r[0]


p1()
p2()
