# @formatter:off
from os.path import isfile, join as path_join
from sys import path as sys_path
sys_path.insert(1, path_join(sys_path[0], '..'))
file_name = path_join('input', 'day18.txt')
def to_list(mf=int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]
def to_gen(mf=int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)
def p1(*args): ans = part1(*args); print(ans); return ans
def p2(*args): ans = part2(*args); print(ans); return ans

if not isfile(file_name):
	from aoc import get_input_file
	get_input_file(session_path=['..', '.env'])
# @formatter:on

from utils import *

data = parsefile(file_name,  [[int, ","], "\n"])

w = 71
h = 71
	
count = 1024

import heapq

def dfs(start, end, grid):
	seen = set()
	
	scores = {}
	scores[start] = 0
	to_check = [(0, start)]
	
	
	while len(to_check):
		score, curr = heapq.heappop(to_check)
		
		seen.add(curr)
		
		for dx, dy in ((0, 1), (0, -1), (-1, 0), (1, 0)):
			nx = curr[0] + dx
			ny = curr[1] + dy
			
			if nx >= 0 and nx < w and ny >= 0 and ny <h and (nx, ny) not in grid:
				ns = score+1
				
				if (nx, ny) == end:
					return ns
				
				if (nx, ny) not in scores or ns < scores[(nx, ny)]:
					heapq.heappush(to_check, (ns, (nx, ny)))
					scores[(nx, ny)] = ns
	
	return None

		
def part1():
	bs = set([tuple(d) for d in data[:count]])
	r = dfs((0, 0), (w-1, h-1), bs)
	return r


def part2():
	bs = set([tuple(d) for d in data[:count]])
	for i, b in enumerate(data[count:]):
		bs.add(tuple(b))
		r = dfs((0, 0), (w-1, h-1), bs)
		if r is None:
			return str(b[0]) + "," + str(b[1])
	return None


p1()
p2()
