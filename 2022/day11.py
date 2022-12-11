# @formatter:off
from os.path import isfile, join as path_join
from sys import path as sys_path
sys_path.insert(1, path_join(sys_path[0], '..'))
file_name = path_join('input', 'day11.txt')
def to_list(mf: object = int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]
def to_gen(mf: object = int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)
def p1(*args): ans = part1(*args); print(ans); return ans
def p2(*args): ans = part2(*args); print(ans); return ans

if not isfile(file_name):
	from aoc import get_input_file
	get_input_file(session_path=['..', '.env'])
# @formatter:on

from utils import parsefile

data = parsefile(file_name, [str, "\n\n"])

monkeys = []

for d in data:
	lines = d.split("\n")
	
	id = int(lines[0].split(" ")[1][:-1])
	items = [int(i.strip()) for i in lines[1].split(":")[1].split(",")]
	cl = lines[2].split("=")[1].strip().split(" ")
	change = [0, 0, 0]
	if cl[0] == "old":
		change[0] = 0
	else:
		change[0] = int(cl[0])
		
	if cl[2] == "old":
		change[2] = 0
	else:
		change[2] = int(cl[2])
		
	if cl[1] == "+":
		change[1] = 0
	else:
		change[1] = 1
		
	div = int(lines[3].split()[-1])
	test_true = int(lines[4].split()[-1])
	test_false = int(lines[5].split()[-1])
	
	monkeys.append([id, items, change, div, test_true, test_false])

from math import prod

divisor = prod([m[3] for m in monkeys])

def round(monkeys, count, skip_div=False):
	for m in monkeys:
		for item in m[1]:
			count[m[0]] += 1
			wl = item
			
			nums = [wl, wl]
			if m[2][0] != 0:
				nums[0] = m[2][0]
			if m[2][2] != 0:
				nums[1] = m[2][2]
		
			if m[2][1] == 0:
				wl = nums[0] + nums[1]
			else:
				wl = nums[0] * nums[1]
			
			if not skip_div:
				wl //= 3
			
			if skip_div:
				wl %= divisor
			
			if wl % m[3] == 0:
				monkeys[m[4]][1].append(wl)
			else:
				monkeys[m[5]][1].append(wl)
			
		m[1] = []

from copy import deepcopy

def part1():
	monks = deepcopy(monkeys)
	count = {i:0 for i in range(len(monks))}
	
	for i in range(20):
		round(monks, count)
		
	c = sorted(list(count.values()), reverse=True)
	return c[0] * c[1]

def part2():
	monks = deepcopy(monkeys)
	count = {i:0 for i in range(len(monks))}
	
	for i in range(10000):
		round(monks, count, True)
	
	c = sorted(list(count.values()), reverse=True)
	return c[0] * c[1]


p1()
p2()
