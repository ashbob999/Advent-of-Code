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

coords = parsefile(file_name,  [[int, ", "], "\n"])

w = max(c[0] for c in coords)+2
h = max(c[1] for c in coords)+2

g = [[{} for x in range(w)] for y in range(h)]

for i, coord in enumerate(coords):
	print(i)
	for y in range(h):
		for x in range(w):
			dist = abs(coord[0] - x) + abs(coord[1] - y)
			
			if dist not in g[y][x]:
				g[y][x][dist] = set()
				
			g[y][x][dist].add(i)

def part1():
	nums = set([i for i in range(len(coords))])
	
	def do_remove(dists):
		mv = min(dists.items(), key=lambda x:x[0])
		if len(mv[1]) == 1:
			n = list(mv[1])[0]
			if n in nums:
				nums.remove(n)
	
	for x in range(w):
		dists = g[0][x]
		do_remove(dists)
		
	for x in range(w):
		dists = g[h-1][x]
		do_remove(dists)
		
	for y in range(w):
		dists = g[y][0]
		do_remove(dists)
		
	for y in range(w):
		dists = g[y][w-1]
		do_remove(dists)
		
	counts = {}
	
	for y in range(h):
		for x in range(w):
			dists = g[y][x]
			mv = min(dists.items(), key=lambda x:x[0])
			if len(mv[1]) == 1:
				n = list(mv[1])[0]
				if n not in counts:
					counts[n] = 0
				counts[n] += 1
	
	return max([v for v in counts.items() if v[0] in nums], key=lambda x:x[1])[1]
		

def part2():
	count = 0
	
	print(g[3][4])
	
	for y in range(h):
		for x in range(w):
			dists = g[y][x]
			
			s = sum(v[0] * len(v[1]) for v in dists.items())
			if s < 10000:
				count += 1
			
	return count


p1()
p2()
