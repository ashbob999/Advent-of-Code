# @formatter:off
from os.path import isfile, join as path_join
from sys import path as sys_path
sys_path.insert(1, path_join(sys_path[0], '..'))
file_name = path_join('input', 'day10.txt')
def to_list(mf=int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]
def to_gen(mf=int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)
def p1(*args): ans = part1(*args); print(ans); return ans
def p2(*args): ans = part2(*args); print(ans); return ans

if not isfile(file_name):
	from aoc import get_input_file
	get_input_file(session_path=['..', '.env'])
# @formatter:on

from utils import *

from heapq import *

data = parsefile(file_name, "\n")

raw = """[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}"""
data = parse(raw, "\n")

jolts = []
for d in data:
	parts = d.split()
	
	ind_str = list(parts[0][1:-1])
	ind = [c == "#" for c in ind_str]
	
	btns = [list(map(int, v[1:-1].split(","))) for v in parts[1:-1]]
	
	jr = list(map(int, parts[-1][1:-1].split(",")))
	
	jolt = (ind, btns, jr)
	jolts.append(jolt)
	#print(jolt)

print(len(jolts))

def close(val):
	s = 0
	for v in val:
		if v:
			s += 1
	return s


def press(val, btns):
	res = val[:]
	for btn in btns:
		res[btn] = not res[btn]
	return res

def check(val):
	return all(v == False for v in val)

def bfs(start, btns):
	
	seen = {}
	to_check = [(0, close(start), start, None)]
	
	while len(to_check):
		cp, cc, cv, pb = heappop(to_check)

		seen[tuple(cv)] = cp

		for btn in btns:
			if btn == pb:
				continue
			
			nv = press(cv, btn)
			dist = close(nv)
			
			if tuple(nv) in seen:
				if seen[tuple(nv)] < cp+1:
					continue
			
			if check(nv):
				return cp+1
			
			heappush(to_check, (cp+1, dist, nv, btn))



def part1():
	s=  0
	for i, j in enumerate(jolts):
		print(i)
		res = bfs(j[0], j[1])
		s += res
	return s



def close2(val):
	return sum(val)

def press2(val, btns):
	res = val[:]
	for btn in btns:
		res[btn] -= 1
	return res
	
def check2(val):
	return all(v == 0 for v in val)

def fail(val):
	return any(v < 0 for v in val)

def bfs2(start, btns):
	
	seen = {}
	#to_check = [(0, close2(start), start)]
	to_check = [(close2(start), 0, start)]
	
	while len(to_check):
		#cp, cc, cv = heappop(to_check)
		cc, cp, cv = heappop(to_check)

		seen[tuple(cv)] = cp

		for btn in btns:
			nv = press2(cv, btn)
			dist = close2(nv)
			
			if tuple(nv) in seen:
				if seen[tuple(nv)] < cp+1:
					continue
			
			if check2(nv):
				return cp+1
			
			if fail(nv):
				continue
			
			#heappush(to_check, (cp+1, dist, nv))
			heappush(to_check, (dist, cp+1, nv))


import sympy as sp

def sz3(btns, target):
	vals = []
	for v in btns:
		val = [0] * len(target)
		for idx in v:
			val[idx] = 1
		vals.append(val)
		
	print(target, btns)
	print(vals)
	
	sbls = []
	for i in range(len(vals)):
		c = chr(ord("a") + i)
		sbl = sp.symbols(c)
		sbls.append(sbl)
	
	eqs = []
	for ei in range(len(target)):
		pe = None
		for i, v in enumerate(vals):
			if pe is None:
				pe = sbls[i] * v[ei]
			else:
				pe = pe + (sbls[i] * v[ei])
			print("pe", pe)
		
		eq = sp.Eq(pe, target[ei])
		print(eq)
	
	res = sp.solve(eqs, sbls)
	print(res)
	
	return 0



def part2():
	s=  0
	for i, j in enumerate(jolts):
		print(i)
		#res = bfs2(j[2], j[1])
		res = sz3(j[1], j[2])
		print()
		break
		s += res
	return s


#p1()
p2()
