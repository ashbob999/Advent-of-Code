# @formatter:off
from os.path import isfile, join as path_join
from sys import path as sys_path
sys_path.insert(1, path_join(sys_path[0], '..'))
file_name = path_join('input', 'day19.txt')
def to_list(mf=int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]
def to_gen(mf=int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)
def p1(*args): ans = part1(*args); print(ans); return ans
def p2(*args): ans = part2(*args); print(ans); return ans

if not isfile(file_name):
	from aoc import get_input_file
	get_input_file(session_path=['..', '.env'])
# @formatter:on

from utils import *

patterns, towels = parsefile(file_name,  [[", "], 1, ["\n"], "\n\n"])

patterns = sorted(patterns, key=len, reverse=True)

mem1 = {}

def check(towel, ps):
	if (towel, ps) in mem1:
		return mem1[(towel, ps)]
	
	if len(towel) == 0:
		return True
	
	for p in ps:
		if towel.startswith(p):
			r = check(towel[len(p):], ps)
			if r:
				mem1[(towel, ps)]=True
				return True
	mem1[(towel,ps)]=False
	return False

def part1():
	c = 0
	
	for i, t in enumerate(towels):
		ps = tuple([p for p in patterns if p in t])
		if check(t, ps):
			c += 1
			
	return c

	
mem2 = {}
def check2(towel, ps):
	if (towel, ps) in mem2:
		return mem2[(towel, ps)]
	
	if len(towel) == 0:
		return 1
	
	perms = 0 
	
	for p in ps:
		if towel.startswith(p):
			r = check2(towel[len(p):], ps)
			if r > 0:
				perms += r
	
	mem2[(towel,ps)]=perms
	return perms


def part2():
	c = 0
	
	for i, t in enumerate(towels):
		ps = tuple([p for p in patterns if p in t])
		c += check2(t, ps)
			
	return c


p1()
p2()
