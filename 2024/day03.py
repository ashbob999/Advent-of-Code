# @formatter:off
from os.path import isfile, join as path_join
from sys import path as sys_path
sys_path.insert(1, path_join(sys_path[0], '..'))
file_name = path_join('input', 'day03.txt')
def to_list(mf=int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]
def to_gen(mf=int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)
def p1(*args): ans = part1(*args); print(ans); return ans
def p2(*args): ans = part2(*args); print(ans); return ans

if not isfile(file_name):
	from aoc import get_input_file
	get_input_file(session_path=['..', '.env'])
# @formatter:on

from utils import *

data = parsefile(file_name,  None)

from re import findall

def mul(a, b):
	return a * b

mults = []

def part1():
	s = 0
	
	global mults
	mults = findall("mul\\(\\d+,\\d+\\)", data)
	
	for m in mults:
		s += eval(m)
		if data.count(m) >1:
			assert()
		
	return s

def al(data, txt):
	ix = []
	for i in range(len(data)):
		if data[i:i+len(txt)] == txt:
			ix.append(i)
	return ix

def part2():
	indexes = [(data.index(m), 0, m) for m in mults]
	dos = [(i, 1) for i in al(data, "do()")]
	donts = [(i, 2) for i in al(data, "don't()")]
	
	merge = indexes  + dos + donts
	
	state = True
	s = 0
	
	merge = sorted(merge, key=lambda x: x[0])
	
	for v in merge:
		if v[1] == 0:
			if state:
				s += eval(v[2])
		elif v[1]== 1:
			state = True
		elif v[1] == 2:
			state= False
			
	return s


p1()
p2()
