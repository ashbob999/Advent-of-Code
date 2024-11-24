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

poly_ = parsefile(file_name, None)
#poly_ = "dabAcCaCBAcCcaDA"

min_poly = None

def shrink(poly):
	while True:
		has_match = False
		for i in range(0, len(poly) -1):
			if poly[i] != poly[i+1] and poly[i].lower() == poly[i+1].lower():
				has_match = True
				poly = poly[:i] + poly[i+2:]
				break
				
		#if len(poly) % 1000 == 0:print(len(poly))
		if not has_match:
			break
			
	return poly

def part1():
	global min_poly
	min_poly = shrink(poly_)
	return len(min_poly)


def part2():
	min_l = 10000000
	
	for ci in range(ord("a"), ord("z")+1):
		c = chr(ci)
		
		poly = min_poly.replace(c.lower(), "").replace(c.upper(), "")
		
		l = len(shrink(poly))
		
		if l < min_l:
			min_l = l
		
	return min_l

p1()
p2()
