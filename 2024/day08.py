# @formatter:off
from os.path import isfile, join as path_join
from sys import path as sys_path
sys_path.insert(1, path_join(sys_path[0], '..'))
file_name = path_join('input', 'day08.txt')
def to_list(mf=int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]
def to_gen(mf=int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)
def p1(*args): ans = part1(*args); print(ans); return ans
def p2(*args): ans = part2(*args); print(ans); return ans

if not isfile(file_name):
	from aoc import get_input_file
	get_input_file(session_path=['..', '.env'])
# @formatter:on

from utils import *

data = parsefile(file_name, ["\n"])

w = len(data[0])
h = len(data)

ants = {}
for y in range(h):
	for x in range(w):
		if data[y][x] != ".":
			c = data[y][x]
			
			if c not in ants:
				ants[c] = []
				
			ants[c].append((x, y))

def part1():
	antinodes = set()
	
	for ant, poses in ants.items():
		if len(poses) < 2:
			continue
			
		for i in range(len(poses)):
			for j in range(i+1, len(poses)):
				p1 = poses[i]
				p2 = poses[j]
				
				diff = (p1[0] - p2[0], p1[1] - p2[1])
				
				n1 = (p1[0] + diff[0], p1[1] + diff[1])
				n2 = (p2[0] - diff[0], p2[1] - diff[1])
				
				if n1[0] >= 0 and n1[0] < w and n1[1] >= 0 and n1[1] < h:
					antinodes.add(n1)
				
				if n2[0] >= 0 and n2[0] < h and n2[1] >= 0 and n2[1] < h:
					antinodes.add(n2)
				
	
	return len(antinodes)


def part2():
	antinodes = set()
	
	for ant, poses in ants.items():
		if len(poses) < 2:
			continue
			
		for i in range(len(poses)):
			for j in range(i+1, len(poses)):
				p1 = poses[i]
				p2 = poses[j]
				
				diff = (p1[0] - p2[0], p1[1] - p2[1])
				
				for k in range(0, 100):
				
					n1 = (p1[0] + diff[0]*k, p1[1] + diff[1]*k)
					n2 = (p2[0] - diff[0]*k, p2[1] - diff[1]*k)
				
					n1out = False
					n2out = False
				
					if n1[0] >= 0 and n1[0] < w and n1[1] >= 0 and n1[1] < h:
						antinodes.add(n1)
					else:
						n1put = True
				
					if n2[0] >= 0 and n2[0] < h and n2[1] >= 0 and n2[1] < h:
						antinodes.add(n2)
					else:
						n2out = True
						
					if n1out and n2out:
						break
				
	
	return len(antinodes)


p1()
p2()
