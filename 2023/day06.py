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

from utils import *

data = parsefile(file_name,  [[None, 1, int, 0], "\n"])


"""
	y: dist
	x: time pressed
	
	y = x * (tot_time - x)
	y = tot_time*x - x*x
	
	max_dist < tot_time*x - x*x
	max_dist = tot_time*x - x*x
	0 = tot_time*x - x*x - max_dist
"""
def quad(a, b, c):
	# quadratic equation
	det = (b**2 - 4.0000001*a*c) ** 0.5
	den = 2*a
	
	x1 = (-b + det) / den
	x2 = (-b - det) / den
	return x1, x2

from math import ceil, floor


def part1():
	res = 1
	
	for i in range(len(data[0])):
		time = data[0][i]
		dist = data[1][i]
		
		"""
		wins = 0
		for i in range(time):
			speed = i
			left = time - i
			if left * speed > dist:
				wins += 1
				
		if wins > 0:
			res *= wins
		"""
		
		xv = quad(-1, time, -dist)
		v1 = ceil(xv[0])
		v2 = floor(xv[1])
		wins = v2 - v1 +1
		if wins > 0:
			res *= wins
			
	return res
		

def part2():
	time = int("".join(map(str, data[0])))
	dist = int("".join(map(str, data[1])))
	
	"""
	v1 = None
	for i in range(time):
		speed = i
		left = time - i
		if left * speed > dist:
			v1 =  i
			break
			
	v2 = None
	for i in range(time-1, -1, -1):
		speed = i
		left = time - i
		if left * speed > dist:
			v2 =  i
			break
	"""
	
	# assume xv is sorted
	xv = quad(-1, time, -dist)
	#print(xv)
	v1 = ceil(xv[0])
	v2 = floor(xv[1])
	
	return v2 - v1 +1

p1()
p2()
