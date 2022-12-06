# @formatter:off
from os.path import isfile, join as path_join
from sys import path as sys_path
sys_path.insert(1, path_join(sys_path[0], '..'))
file_name = path_join('input', 'day06.txt')
def to_list(mf: object = int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]
def to_gen(mf: object = int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)
def p1(*args): ans = part1(*args); print(ans); return ans
def p2(*args): ans = part2(*args); print(ans); return ans

if not isfile(file_name):
	from aoc import get_input_file
	get_input_file(session_path=['..', '.env'])
# @formatter:on

from utils import parsefile

data = parsefile(file_name, None)

def part1():
	s = set()
	for i in range(len(data)-4):
		s=set()
		for j in range(i, i+4):
			s.add(data[j])
		if len(s)==4:
			return i+4

def part2():
	s = set()
	for i in range(len(data)-14):
		s=set()
		for j in range(i, i+14):
			s.add(data[j])
		if len(s)==14:
			return i+14


p1()
p2()
