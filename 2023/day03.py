# @formatter:off
from os.path import isfile, join as path_join
from sys import path as sys_path
sys_path.insert(1, path_join(sys_path[0], '..'))
file_name = path_join('input', 'day03.txt')
def to_list(mf: object = int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]
def to_gen(mf: object = int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)
def p1(*args): ans = part1(*args); print(ans); return ans
def p2(*args): ans = part2(*args); print(ans); return ans

if not isfile(file_name):
	from aoc import get_input_file
	get_input_file(session_path=['..', '.env'])
# @formatter:on

from utils import *

data = parsefile(file_name,  [[""], "\n"])

width = len(data[0])
height = len(data)

def part1():
	sum = 0
	
	for y in range(height):
		v = 0
		has_symbol = False
		for x in range(width):
			c = data[y][x]
			if c.isdigit():
				v = v * 10 + int(c)
				
				for i in (-1, 0, 1):
					for j in (-1, 0, 1):
						if 0 <= x+i < width and 0 <= y+j < height:
							c2 = data[y+j][x+i]
							if not c2.isdigit() and c2 != ".":
								has_symbol = True
			else:
				if has_symbol:
					sum += v
				v = 0
				has_symbol = False
		
		if has_symbol:
			sum += v
			
	return sum


def part2():
	sum = 0
	
	mults = {}
	
	for y in range(height):
		v = 0
		has_mult = False
		mult_pos=set()
		for x in range(width):
			c = data[y][x]
			if c.isdigit():
				v = v * 10 + int(c)
				
				for i in (-1, 0, 1):
					for j in (-1, 0, 1):
						if 0 <= x+i < width and 0 <= y+j < height:
							c2 = data[y+j][x+i]
							if c2 == "*":
								has_mult = True
								mult_pos.add((x+i, y+j))
			else:
				if has_mult:
					for m in mult_pos:
						if m not in mults:
							mults[m] = []
						mults[m].append(v)
					
				v = 0
				has_mult = False
				mult_pos = set()
		
		if has_mult:
			for m in mult_pos:
				if m not in mults:
					mults[m] = []
			mults[m].append(v)
	
	for p, poses in mults.items():
		if len(poses) == 2:
			sum += poses[0] * poses[1]
	
	return sum


p1()
p2()
