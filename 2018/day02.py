# @formatter:off
from os.path import isfile, join as path_join
from sys import path as sys_path
sys_path.insert(1, path_join(sys_path[0], '..'))
file_name = path_join('input', 'day02.txt')
def to_list(mf=int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]
def to_gen(mf=int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)
def p1(*args): ans = part1(*args); print(ans); return ans
def p2(*args): ans = part2(*args); print(ans); return ans

if not isfile(file_name):
	from aoc import get_input_file
	get_input_file(session_path=['..', '.env'])
# @formatter:on

from utils import *


ids = parsefile(file_name, str)


def part1():
	twos = 0
	threes = 0
	
	for id in ids:
		counts = [id.count(c) for c in id]
		if 2 in counts:
			twos += 1
			
		if 3 in counts:
			threes += 1
			
	return twos * threes


def part2():
	vals = [(id, set([(i, c) for i, c in enumerate(id)])) for id in ids]
	
	for v1 in vals:
		for v2 in vals:
			if v1[0] != v2[0]:
				diff = v1[1] ^ v2[1]
				if len(diff) == 2:
					chars = list(v1[1] & v2[1])
					chars = sorted(chars, key=lambda x: x[0])
					return "".join([v[1] for v in chars])
					


p1()
p2()
