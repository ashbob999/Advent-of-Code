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

data = parsefile(file_name, [[str], "\n"])


paths = {}
for d in data:
	paths[d[0][:-1]] = d[1:]


cache = {}
def count(start):
	if start in cache:
		return cache[start]
		
	if start == "out":
		return 1
	
	tp = 0
	for v in paths[start]:
		tp += count(v)
	
	cache[start] = tp
	return tp


def part1():
	return count("you")


cache2_do = {}
def do_check(start):
	has_mat = [False, False]
	if start in cache2_do:
		r = cache2_do[start]
		return r
	
	if start == "out":
		cache2_do[start] = [False, False]
		return [False, False]

	
	for v in paths[start]:
		hm = do_check(v)
		#print("do", start)

		if hm[0]:
			has_mat[0] = True
		if hm[1]:
			has_mat[1] = True

	if start == "fft":
		has_mat[0] = True
	if start == "dac":
		has_mat[1] = True
	
	cache2_do[start] = has_mat
	return has_mat


cache2 = {}
def count2(start, has_mat):
	has_mat = has_mat[:]
	
	if start in cache2:
		return cache2[start]
	
	if start == "out":
		return 1
	
	if start == "fft":
		has_mat[0] = True
	if start == "dac":
		has_mat[1] = True
	
	tp = 0
	for v in paths[start]:
		hm = cache2_do[v]
		
		cm = [has_mat[0] or hm[0], has_mat[1] or hm[1]]
		if not cm[0] or not cm[1]:
			continue
		
		c = count2(v, has_mat)

		tp += c
		
		if hm[0] and hm[1]:
			cache2[v] = c
	
	if tp > 0:
		cache2[start] = tp
	
	return tp


def part2():
	do_check("svr")
	
	res = count2("svr", [False, False])
	return res


p1()
p2()
