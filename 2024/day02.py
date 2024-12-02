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

levels = parsefile(file_name,  [[int], "\n"])

def safe(level):
	s1 = sorted(level)
	s2 = sorted(level, reverse=True)
	
	if level != s1 and level != s2:
		return False
		
	for i in range(len(level)-1):
		diff = abs(level[i+1] - level[i])
		if diff > 3 or diff < 1:
			return False
	
	return True

def part1():
	s = 0
	for l in levels:
		if safe(l):
			s += 1
	return s


def part2():
	s = 0
	for level in levels:
		if safe(level):
			s += 1
		else:
			for i in range(len(level)):
				nl = level[:i] + level[i+1:]
				if safe(nl):
					s += 1
					break
	return s


p1()
p2()
