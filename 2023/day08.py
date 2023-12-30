# @formatter:off
from os.path import isfile, join as path_join
from sys import path as sys_path
sys_path.insert(1, path_join(sys_path[0], '..'))
file_name = path_join('input', 'day08.txt')
def to_list(mf: object = int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]
def to_gen(mf: object = int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)
def p1(*args): ans = part1(*args); print(ans); return ans
def p2(*args): ans = part2(*args); print(ans); return ans

if not isfile(file_name):
	from aoc import get_input_file
	get_input_file(session_path=['..', '.env'])
# @formatter:on

from utils import *

data = parsefile(file_name,  [str, 1, [[str, "="], "\n"], 0, "\n\n"])

steps = data[0]

nodes = {}

for d in data[1]:
	#print(d)
	start = d[0].strip()
	
	vals = d[1].strip().split(",")
	left = vals[0].replace("(", "").strip()
	right = vals[1].replace(")", "").strip()
	
	nodes[start] = (left, right)

def part1():
	count =0
	
	node = "AAA"
	
	i=0
	while node != "ZZZ":
		if i >= len(steps):
			i = 0
			
		c = steps[i]
		if c == "L":
			node = nodes[node][0]
		else:
			node = nodes[node][1]
			
		i+=1
		count +=1
	
	return count


try:
	from math import lcm
except Exception as e:
	from math import gcd  # Python versions 3.5 and above
	# from fractions import gcd # Python versions below 3.5
	from functools import reduce  # Python version 3.x

	def lcm(*denominators):
		return reduce(lambda a, b: a * b // gcd(a, b), denominators)


def part2():
	count =0
	
	st_nodes = [k for k in nodes.keys() if k[2]=="A"]
	st_cnt = len(st_nodes)
	
	step_cnt = len(steps)
	
	st_nodes_cycles = {}
	
	for st in st_nodes:
		n = st
		c1 = 0
		c2 = 0
		i = 0
		while n[2] != "Z":
			if i >= step_cnt:
				i = 0
				
			c = steps[i]
			if c == "L":
				n = nodes[n][0]
			else:
				n = nodes[n][1]
			
			c1 += 1
			i += 1
		
		c2 = 1

		if i >= step_cnt:
			i = 0
		c = steps[i]
		if c == "L":
			n = nodes[n][0]
		else:
			n = nodes[n][1]
		i+= 1
		
		while n[2] != "Z":
			if i >= step_cnt:
				i = 0
				
			c = steps[i]
			if c == "L":
				n = nodes[n][0]
			else:
				n = nodes[n][1]
			
			c2 += 1
			i += 1
			
		st_nodes_cycles[st] = (c1, c2)
	
	# do lcm on cycle lengths
	# ignoring offsets for some reason?
	count = lcm(*[x[1] for x in st_nodes_cycles.values()])
	
	return count


p1()
p2()
