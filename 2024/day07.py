# @formatter:off
from os.path import isfile, join as path_join
from sys import path as sys_path
sys_path.insert(1, path_join(sys_path[0], '..'))
file_name = path_join('input', 'day07.txt')
def to_list(mf=int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]
def to_gen(mf=int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)
def p1(*args): ans = part1(*args); print(ans); return ans
def p2(*args): ans = part2(*args); print(ans); return ans

if not isfile(file_name):
	from aoc import get_input_file
	get_input_file(session_path=['..', '.env'])
# @formatter:on

from utils import *

data = parsefile(file_name,  [[int, [int], ": "], "\n"])


def check1(t, v, left):
	if v > t:
		return False
	
	if len(left) == 0:
		if v == t:
			return True
		return False
	
	v1 = v + left[0]
	if v1 <= t:
		if check1(t, v1, left[1:]):
			return True
	
	v2 = v * left[0]
	if v2 <= t:
		if check1(t, v2, left[1:]):
			return True
	
	
	return False

def check2(t, v, left):
	if v > t:
		return False
	
	if len(left) == 0:
		if v == t:
			return True
		return False
	
	v1 = v + left[0]
	if v1 <= t:
		if check2(t, v1, left[1:]):
			return True
	
	v2 = v * left[0]
	if v2 <= t:
		if check2(t, v2, left[1:]):
			return True
			
	v3 = int(str(v) + str(left[0]))
	if v3 <= t:
		if check2(t, v3, left[1:]):
			return True
	
	
	return False


def part1():
	s = 0
	
	for d in data:
		if check1(d[0], d[1][0], d[1][1:]):
			s += d[0]
			
	return s


def part2():
	s = 0
	
	for d in data:
		if check2(d[0], d[1][0], d[1][1:]):
			s += d[0]

	return s

p1()
p2()
