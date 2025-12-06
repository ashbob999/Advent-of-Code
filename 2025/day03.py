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


def largest2(arr, count):
	vals = [0] * (count+1)

	for v in arr:
		print(*vals)
		vals[-1] = v

		for j in range(1, count+1):
			if vals[j - 1] < vals[j]:
				vals.pop(j-1)
				vals.append(v)
				break

	return sum(vals[i]*(10**(count-i-1)) for i in range(count))


def part2():
	s = 0
	for arr in data:
		v = largest2(arr, 12)
		s += v
		print(v)
	return s


p1()
p2()
