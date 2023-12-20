# @formatter:off
from os.path import isfile, join as path_join
from sys import path as sys_path
sys_path.insert(1, path_join(sys_path[0], '..'))
file_name = path_join('input', 'day20.txt')
def to_list(mf: object = int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]
def to_gen(mf: object = int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)
def p1(*args): ans = part1(*args); print(ans); return ans
def p2(*args): ans = part2(*args); print(ans); return ans

if not isfile(file_name):
	from aoc import get_input_file
	get_input_file(session_path=['..', '.env'])
# @formatter:on

from utils import *

data = parsefile(file_name,  [[str.strip, [str.strip, ","], "->"], "\n"])

conns_ = {}

for d in data:
	type = None
	name = d[0]
	val = None
	if name[0] == "%":
		type = 1 # flip flop
		name = name[1:]
		val = [type, d[1], False]
	elif name[0] == "&":
		type = 2 # conjunction
		name = name[1:]
		val = [type, d[1], {}]
	else:
		type = 0 # broadcast
		val = [type, d[1]]
		
	conns_[name] = val

for k, v in conns_.items():
	if v[0] == 2: # conjunction
		inputs = []
		for k2, v2 in conns_.items():
			if k in v2[1]:
				inputs.append(k2)
				
		v[2] = {v: False for v in inputs}


def pulse(conns, target=None, found=None):
	low = 0
	high = 0
	
	stack = []
	stack.append(("broadcaster", False, "broadcaster"))
	
	while len(stack) > 0:
		curr, signal, prev = stack.pop(0)
		#print(prev, "-"+("high" if signal else "low")+"->", curr)
		
		if target is not None:
			if target == prev:
				if signal:
					found.append(True)
		
		if signal:
			high += 1
		else:
			low += 1
		
		if curr not in conns:
			conns[curr] = [-1, 0, 0]
		val = conns[curr]
			
		type = val[0]
		
		if type == -1:
			continue
		elif type == 0: # broadcast
			for v in val[1]:
				stack.append((v, signal, curr))
		elif type == 1: # flip flop
			if signal == False:
				sig = val[2] == False
				val[2] = not val[2]
				for v in val[1]:
					stack.append((v, sig, curr))
		elif type == 2: # conjunction
			val[2][prev] = signal
			sig = not all(val[2].values())
			for v in val[1]:
				stack.append((v, sig, curr))
	
	return low, high

from copy import deepcopy

def part1():
	conn = deepcopy(conns_)
	
	res = [0, 0]
	for i in range(1000):
		r = pulse(conn, None, None)
		res[0] += r[0]
		res[1] += r[1]
	
	return res[0] * res[1]

from math import prod, lcm

def part2():
	# input that modifies rx
	prev_target = None # conjunction
	for k, v in conns_.items():
		if v[0] == 2:
			if "rx" in v[1]:
				prev_target = k
				break
	
	targets = list(conns_[prev_target][2].keys())
	
	indexes = []
	
	for target in targets:
		conn = deepcopy(conns_)
		i = 0
		while True:
			found = []
			pulse(conn, target, found)
			
			if len(found) > 0:
				indexes.append(i+1)
				break
			
			i += 1
	
	return lcm(*indexes)

p1()
p2()
