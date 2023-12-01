# @formatter:off
from os.path import isfile, join as path_join
from sys import path as sys_path
sys_path.insert(1, path_join(sys_path[0], '..'))
file_name = path_join('input', 'day01.txt')
def to_list(mf: object = int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]
def to_gen(mf: object = int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)
def p1(*args): ans = part1(*args); print(ans); return ans
def p2(*args): ans = part2(*args); print(ans); return ans

if not isfile(file_name):
	from aoc import get_input_file
	get_input_file(session_path=['..', '.env'])
# @formatter:on


from utils import *

data = parsefile(file_name, str)

def part1():
	sum = 0
	
	for line in data:
		v1 = 0
		for c in line:
			if c.isdigit():
				v1 = int(c)
				break
		
		v2 = 0
		for c in line[::-1]:
			if c.isdigit():
				v2 = int(c)
				break
	
		sum += v1 * 10 + v2
	return sum


def part2():
	values = {str(v): v for v in range(10)}
	values["zero"]=0
	values["one"]=1
	values["two"]=2
	values["three"]=3
	values["four"]=4
	values["five"]=5
	values["six"]=6
	values["seven"]=7
	values["eight"]=8
	values["nine"]=9
	
	sum =0
	
	for line in data:
		v1 = min(filter(lambda x: x[0]!=-1, [(line.find(v), v) for v in values]))
		v2 = max(filter(lambda x: x[0]!=-1, [(line.rfind(v), v) for v in values]))
		
		v = values[v1[1]] * 10 + values[v2[1]]
		sum += v
	
	return sum


p1()
p2()
