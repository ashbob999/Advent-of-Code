# @formatter:off
from os.path import isfile, join as path_join
from sys import path as sys_path
sys_path.insert(1, path_join(sys_path[0], '..'))
file_name = path_join('input', 'day10.txt')
def to_list(mf=int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]
def to_gen(mf=int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)
def p1(*args): ans = part1(*args); print(ans); return ans
def p2(*args): ans = part2(*args); print(ans); return ans

if not isfile(file_name):
	from aoc import get_input_file
	get_input_file(session_path=['..', '.env'])
# @formatter:on

from utils import *

g = parsefile(file_name,  [[int, ""], "\n"])

w = len(g[0])
h = len(g)

def check_trail(start):
	
	seen = set(start)
	
	
	to_check = []
	to_check.append(start)
	
	ends = []
	
	while len(to_check):
		curr = to_check.pop(0)
		v = g[curr[1]][curr[0]]
		
		seen.add(curr)
		
		for x in (-1, 1):
			nx = x + curr[0]
			if nx >= 0 and nx < w:
				nv = g[curr[1]][nx]
				if nv == v+1:
					if (nx, curr[1]) not in seen:
						if nv == 9:
							ends.append((nx, curr[1]))
						else:
							to_check.append((nx, curr[1]))
		
		for y in (-1, 1):
			ny = y + curr[1]
			if ny >= 0 and ny < h:
				nv = g[ny][curr[0]]
				if nv == v+1:
					if (curr[0], ny) not in seen:
						if nv == 9:
							ends.append((curr[0], ny))
						else:
							to_check.append((curr[0], ny))
		
		
	return ends
	

def find_trails():
	s = 0
	
	for y in range(h):
		for x in range(w):
			if g[y][x] == 0:
				s += len(set(check_trail((x, y))))
				
	return s
				

def part1():
	return find_trails()


def find_all_trails():
	s = 0
	
	for y in range(h):
		for x in range(w):
			if g[y][x] == 0:
				s += len(check_trail((x, y)))
				
	return s

def part2():
	return find_all_trails()


p1()
p2()
