# @formatter:off
from os.path import isfile, join as path_join
from sys import path as sys_path
sys_path.insert(1, path_join(sys_path[0], '..'))
file_name = path_join('input', 'day12.txt')
def to_list(mf: object = int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]
def to_gen(mf: object = int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)
def p1(*args): ans = part1(*args); print(ans); return ans
def p2(*args): ans = part2(*args); print(ans); return ans

if not isfile(file_name):
	from aoc import get_input_file
	get_input_file(session_path=['..', '.env'])
# @formatter:on

from utils import *

data = parsefile(file_name,  [[str, [int, ","]], "\n"])


mem = {}
def rec_count(arr, counts):
	if (arr, tuple(counts)) in mem:
		return mem[(arr, tuple(counts))]
	
	if len(counts) == 0:
		if "#" in arr:
			# still more # but no counts left
			return 0
		else:
			return 1
	
	# check length is valid
	if len(arr) < counts[0]:
		return 0
	
	count = 0
	
	if not "." in arr[:counts[0]]:
		# check char after count is valud
		if len(arr) == counts[0] or arr[counts[0]] != "#":
			count += rec_count(arr[counts[0]+1:], counts[1:])
	
	if arr[0] != "#":
		count += rec_count(arr[1:], counts[0:])
	
	mem[(arr, tuple(counts))] = count
	return count

def part1():
	c = 0
	for d in data:
		c += rec_count(*d)
	
	return c


def part2():
	c = 0
	
	for d in data:
		arr = "?".join([d[0]]*5)
		counts = d[1]*5
		c += rec_count(arr, counts)
		
	return c


p1()
p2()
