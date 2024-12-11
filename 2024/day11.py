# @formatter:off
from os.path import isfile, join as path_join
from sys import path as sys_path
sys_path.insert(1, path_join(sys_path[0], '..'))
file_name = path_join('input', 'day11.txt')
def to_list(mf=int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]
def to_gen(mf=int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)
def p1(*args): ans = part1(*args); print(ans); return ans
def p2(*args): ans = part2(*args); print(ans); return ans

if not isfile(file_name):
	from aoc import get_input_file
	get_input_file(session_path=['..', '.env'])
# @formatter:on

from utils import *

stones = parsefile(file_name,  [int])

def blink(stones):
	ns = []
	
	for stone in stones:
		if stone == 0:
			ns.append(1)
		#s = str(stone)
		elif len(str(stone)) % 2 == 0:
			s = str(stone)
			ns.append(int(s[:len(s)//2]))
			ns.append(int(s[len(s)//2:]))
		else:
			ns.append(stone * 2024)
		
	
	return ns

def part1():
	s = stones[:]
	
	for i in range(25):
		s = blink(s)
	
	#print(s)
	return len(s)

mem={}

def blink2(v, c):
	if (v, c) in mem:
		return mem[(v, c)]
	
	if c == 0:
		mem[(v, c)] = 1
		return 1
	
	if v == 0:
		r = blink2(1, c - 1)
	elif len(str(v)) %2 == 0:
		s = str(v)
		v1 = int(s[:len(s)//2])
		v2 = int(s[len(s)//2:])
		r = blink2(v1, c - 1) + blink2(v2, c - 1)
	else:
		r = blink2(v * 2024, c - 1)

	mem[(v, c)] = r
	return r

def part2():
	t = 0
	for s in stones:
		v = blink2(s, 75)
		t += v
		
	return t


p1()
p2()
