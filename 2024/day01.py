# @formatter:off
from os.path import isfile, join as path_join
from sys import path as sys_path
sys_path.insert(1, path_join(sys_path[0], '..'))
file_name = path_join('input', 'day01.txt')
def to_list(mf=int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]
def to_gen(mf=int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)
def p1(*args): ans = part1(*args); print(ans); return ans
def p2(*args): ans = part2(*args); print(ans); return ans

if not isfile(file_name):
	from aoc import get_input_file
	get_input_file(session_path=['..', '.env'])
# @formatter:on

from utils import *

vals = parsefile(file_name,  [[int], "\n"])

v1 = [v[0] for v in vals]
v2 = [v[1] for v in vals]

v1 = sorted(v1)
v2 = sorted(v2)

def part1():
	s = 0
	for i in range(len(vals)):
		s += abs(v1[i] - v2[i])
		
	return s


def part2():
	s = set(v1)
	
	t = 0
	
	for v in s:
		t += v2.count(v) * v
	
	return t


p1()
p2()
