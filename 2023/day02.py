# @formatter:off
from os.path import isfile, join as path_join
from sys import path as sys_path
sys_path.insert(1, path_join(sys_path[0], '..'))
file_name = path_join('input', 'day02.txt')
def to_list(mf: object = int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]
def to_gen(mf: object = int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)
def p1(*args): ans = part1(*args); print(ans); return ans
def p2(*args): ans = part2(*args); print(ans); return ans

if not isfile(file_name):
	from aoc import get_input_file
	get_input_file(session_path=['..', '.env'])
# @formatter:on

from utils import *
from math import prod

data = parsefile(file_name, [[[None, 1, int], [[[int, 1, str], ","], ";"], ":"], "\n"])

def part1():
	sum = 0
	
	limits = {"red": 12, "blue": 14, "green": 13}
	
	for id, game in data:
		valid = True
		for s in game:
			for cube in s:
				if cube[0] > limits[cube[1]]:
					valid = False
					break
					
			if not valid:
				break
				
		if valid:
			sum += id[0]
	
	return sum

def part2():
	sum = 0
	
	for id, game in data:
		min_vals = {}
		for s in game:
			for cube in s:
				if cube[1] in min_vals and min_vals[cube[1]] < cube[0]:
					min_vals[cube[1]] = cube[0]
				elif cube[1] not in min_vals:
					min_vals[cube[1]] = cube[0]
		
		sum += prod(min_vals.values())
	
	return sum

p1()
p2()
