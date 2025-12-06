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

data = parsefile(file_name, [[int, ""], "\n"])


def largest(arr):
	val = arr[0] * 10 + arr[1]
	
	for i in range(len(arr)):
		for j in range(i+1, len(arr)):
			v = arr[i] * 10 + arr[j]
			if v > val:
				val = v
				
	return val


def part1():
	s = 0
	for arr in data:
		s += largest(arr)
	return s


cache = {}
def rec(arr, depth, ci, count):
	if (depth, ci) in cache:
		return cache[(depth, ci)]

	if depth > count:
		return None
		
	if ci >= len(arr):
		return None
	
	mx = None
	for i in range(ci, len(arr) - (count - depth)):
		cv = arr[i]
		
		val = None
		if depth == count:
			val = [cv]
		else:
			val = [cv, *rec(arr, depth+1, i+1, count)]
		
		if mx is None:
			mx = val
		else:
			mx = max(mx, val)

	cache[(depth, ci)] = mx
	return mx
	

def largest2(arr, count):
	vals = arr[:count]
	val = arr[0] * 10 + arr[1]
	vals = rec(arr, 1, 0, count)
	#print(vals)
	return sum(vals[i]*(10**(count-i-1)) for i in range(count))


def part2():
	global cache
	s = 0
	for arr in data:
		cache = {}
		s += largest2(arr, 12)
	return s


p1()
p2()
