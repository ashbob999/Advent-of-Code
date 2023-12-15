# @formatter:off
from os.path import isfile, join as path_join
from sys import path as sys_path
sys_path.insert(1, path_join(sys_path[0], '..'))
file_name = path_join('input', 'day15.txt')
def to_list(mf: object = int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]
def to_gen(mf: object = int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)
def p1(*args): ans = part1(*args); print(ans); return ans
def p2(*args): ans = part2(*args); print(ans); return ans

if not isfile(file_name):
	from aoc import get_input_file
	get_input_file(session_path=['..', '.env'])
# @formatter:on

from utils import *

data = parsefile(file_name, ",")


def hash(str):
	curr = 0
	for c in str:
		curr += ord(c)
		curr *= 17
		curr %= 256
		
	return curr


def part1():
	s = 0
	
	for str in data:
		s += hash(str)
	
	return s


def score(map):
	s = 0
	
	for box, v in map.items():
		for i, lens in enumerate(v.items(), 1):
			m1 = box+1
			m2 = i
			m3 = lens[1]
			s += m1 * m2 * m3
			
	return s

def part2():
	map = {}
	
	for str in data:
		label = None
		num = None
		if "=" in str:
			add = True
			label, num = str.split("=")
		elif "-" in str:
			add = False
			label = str.split("-")[0]
		else:
			assert False
		
		if add:
			num = int(num)
		
		box = hash(label)
		
		if add:
			if box not in map:
				map[box] = {}
			map[box][label] = num
		else:
			if box in map:
				if label in map[box]:
					del map[box][label]
					
	return score(map)


p1()
p2()
