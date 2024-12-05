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

rules, order = parsefile(file_name,  [[[int, "|"], "\n"], [[int, ","], "\n"], "\n\n"])

def check(o):
	for i in range(len(o)):
		v = o[i]
		
		for r in rules:
			if r[1] == v:
				if r[0] in o:
					index = o.index(r[0])
					if index > i:
						return False
		
		
	return True

def part1():
	s = 0
	
	for o in order:
		if check(o):
			s += o[len(o) // 2]
	
	return s

def fix(o):
	new_o = []
	
	rs = [r for r in rules if r[0] in o and r[1] in o]
	
	for v in o:
		idxs = [(new_o.index(r[0]) if r[0] in new_o else -1) for r in rs if r[1] == v]
		index = max(idxs if len(idxs) else [-1]) + 1
		new_o.insert(index, v)
	
	assert len(o) == len(new_o)
	assert check(new_o)
	return new_o

def part2():
	s = 0
	
	for o in order:
		if not check(o):
			new_o = fix(o)
			s += new_o[len(o) // 2]
	
	return s


p1()
p2()
