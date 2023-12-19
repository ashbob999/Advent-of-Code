# @formatter:off
from os.path import isfile, join as path_join
from sys import path as sys_path
sys_path.insert(1, path_join(sys_path[0], '..'))
file_name = path_join('input', 'day19.txt')
def to_list(mf: object = int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]
def to_gen(mf: object = int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)
def p1(*args): ans = part1(*args); print(ans); return ans
def p2(*args): ans = part2(*args); print(ans); return ans

if not isfile(file_name):
	from aoc import get_input_file
	get_input_file(session_path=['..', '.env'])
# @formatter:on

from utils import *

data = parsefile(file_name,  [[str, "\n"], [str, "\n"], "\n\n"])

workflows = {}
for d in data[0]:
	name, steps = d.split("{")
	steps = steps[:-1]
	steps = steps.split(",")
	
	res = []
	for step in steps:
		if ":" not in step:
			res.append(step)
			continue
		
		cond, end = step.split(":")
		if "<" in cond:
			k, v = cond.split("<")
			type = 0
		elif ">" in cond:
			k, v = cond.split(">")
			type = 1
		else:
			assert False
		v = int(v)
		
		res.append((k, v, type, end))
		
	workflows[name] = res
	
parts = []
for d in data[1]:
	d = d[1:-1]
	sections = d.split(",")
	
	part = {}
	
	for section in sections:
		k, v = section.split("=")
		part[k] = int(v)
	
	parts.append(part)


def check(part, curr):
	if curr == "A":
		return True
	elif curr == "R":
		return False
		
	steps = workflows[curr]
	for step in steps:
		if isinstance(step, tuple):
			if step[2] == 0: # lt
				if part[step[0]] < step[1]:
					return check(part, step[3])
			else: # gt
				if part[step[0]] > step[1]:
					return check(part, step[3])
				
		else:
			return check(part, step)

def part1():
	matches = []
	for part in parts:
		if check(part, "in"):
			matches.append(part)
			
	return sum([sum(part.values()) for part in matches])

from math import prod

def copyv(val):
	return {k: v[:] for k, v in val.items()}

# x,m,a,s 0-4000 inc/inc
def count(vals, curr):
	for v in vals.values():
		if v[1] <= v[0]:
			return 0
	
	if curr == "A":
		p = prod([v[1] - v[0] for v in vals.values()])
		return p
	elif curr == "R":
		return 0
		
	vals = copyv(vals)
	
	c = 0
	
	steps = workflows[curr]
	for step in steps:
		if isinstance(step, tuple):
			v2 = copyv(vals)
			if step[2] == 0: # lt
				v2[step[0]][1] = min(v2[step[0]][1], step[1])
				vals[step[0]][0] = max(v2[step[0]][0], step[1])
			else: # gt
				v2[step[0]][0] = max(v2[step[0]][0], step[1]+1)
				vals[step[0]][1] = min(v2[step[0]][1], step[1]+1)
			
			c += count(v2, step[3])
		else:
			c += count(vals, step)
		
	return c


def part2():
	minv = 1
	maxv = 4000+1
	vals = {v: [minv, maxv] for v in "xmas"}
	
	res = count(vals, "in")
	return res


p1()
p2()
