# @formatter:off
from os.path import isfile, join as path_join
from sys import path as sys_path
sys_path.insert(1, path_join(sys_path[0], '..'))
file_name = path_join('input', 'day05.txt')
def to_list(mf=int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]
def to_gen(mf=int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)
def p1(*args): ans = part1(*args); print(ans); return ans
def p2(*args): ans = part2(*args); print(ans); return ans

if not isfile(file_name):
	from aoc import get_input_file
	get_input_file(session_path=['..', '.env'])
# @formatter:on

from utils import *

ranges, ids = parsefile(file_name, [[[int, "-"], "\n"], 1, [int, "\n"], 1, "\n\n"])


def part1():
	c = 0
	
	for id in ids:
		for r in ranges:
			if id >= r[0] and id <= r[1]:
				c += 1
				break
	
	return c


def part2():
	rngs = sorted(ranges)
	
	i = 0
	while i < len(rngs)-1:
		r1 = rngs[i]
		r2 = rngs[i+1]
		
		
			
		if r1 == r2:
			rngs.pop(i+1)
			continue
			
		if r1[0] == r2[0]:
			rngs.pop(i)
			continue
			
		if r1[1] >= r2[1]:
			rngs.pop(i+1)
			continue
		
		
		if r1[1] >= r2[0]:
			rngs[i][1] = r2[1]
			rngs.pop(i+1)
			continue
		
		i += 1
		
	c = 0
	
	for r in rngs:
		c += r[1] - r[0] + 1
		
	return c


p1()
p2()
