# @formatter:off
from os.path import isfile, join as path_join
from sys import path as sys_path
sys_path.insert(1, path_join(sys_path[0], '..'))
file_name = path_join('input', 'day06.txt')
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

g = set()
start = None 
for y in range(h):
	for x in range(w):
		if data[y][x] == "#":
			g.add((x, y))
		if data[y][x] == "^":
			start = (x, y)

dirs = ((0, -1), (1, 0), (0, 1), (-1, 0))


def cycle(g, start, dir):
	curr = start
	#dir = 0 # up
	
	seen = set()
	seen.add((curr, dir))
	
	r1 = None
	
	while True:
		next = (curr[0] + dirs[dir][0], curr[1] + dirs[dir][1])
		
		if next not in g:
			curr = next
		else:
			dir = (dir + 1) % 4
		
		if curr[0] < 0 or curr[0] >= w or curr[1] < 0 or curr[1] >= h:
			r1 = False
			break
		
		if (curr, dir) in seen:
			r1 = True
			break
		else:
			seen.add((curr, dir))
			
	return seen, r1

def part1():
	seen, r = cycle(g, start, 0)
		
	return len(set([s[0] for s in seen]))

def cycle_rec(g, sofar, rec=False):
	c = set()
	curr, dir = sofar[-1]
	
	seen = set(sofar)
	sp = set([s[0] for s in sofar])
	r1 = None
	
	if curr[0] < 0 or curr[0] >= w or curr[1] < 0 or curr[1] >= h:
		r1 = False
		return c, r1
	
	while True:
		next = (curr[0] + dirs[dir][0], curr[1] + dirs[dir][1])
		
		if rec and next not in sp and c not in next and next not in g:
			ng = g.copy()
			ng.add(next)
			r = cycle_rec(ng, sofar[:], rec=False)

			if r[1]:
				c.add(next)
		
		if next not in g:
			curr = next
		else:
			dir = (dir + 1) % 4
		
		if curr[0] < 0 or curr[0] >= w or curr[1] < 0 or curr[1] >= h:
			r1 = False
			break
		
		if (curr, dir) in seen:
			r1 = True
			break
		else:
			sofar.append((curr, dir))
			seen.add((curr, dir))
			sp.add(curr)
			
	return c, r1

def part2():
	r, _ = cycle_rec(g.copy(), [(start, 0)], rec=True)
	return len(r)


p1()
p2()
