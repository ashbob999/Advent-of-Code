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

data = parsefile(file_name, [[int, "-"], ","])


def checkinvalid(v):
	s = str(v)
	sl = len(s)
	if sl % 2 != 0:
		return False
	return s[:sl//2] == s[sl//2:]

def getinvalid(low, up):
	d1 = len(str(low))
	d2 = len(str(up))
	
	invs = []
	
	for v in range(low, up+1):
		if checkinvalid(v):
			invs.append(v)
	
	return invs


def part1():
	s = 0
	
	for low, up in data:
		for v in getinvalid(low, up):
			s += v
	
	return s


def checkinvalid2(v):
	s = str(v)
	
	l = len(s)
	l2 = l // 2
	
	for i in range(1, l2+1):
		if l % i != 0:
			continue
		
		ls = l // i
		start = s[:i]
		if all(s[i*(ii+1):i*(ii+2)] == start for ii in range(ls-1)):
			return True
		
	return False
	
	return s[:len(s)//2] == s[len(s)//2:]

def getinvalid2(low, up):
	d1 = len(str(low))
	d2 = len(str(up))
	
	invs = []
	
	for v in range(low, up+1):
		if checkinvalid2(v):
			invs.append(v)
	
	return invs


def part2():
	s = 0
	
	for low, up in data:
		for v in getinvalid2(low, up):
			s += v
	
	return s

p1()
p2()
