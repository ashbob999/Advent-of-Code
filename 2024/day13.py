# @formatter:off
from os.path import isfile, join as path_join
from sys import path as sys_path
sys_path.insert(1, path_join(sys_path[0], '..'))
file_name = path_join('input', 'day13.txt')
def to_list(mf=int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]
def to_gen(mf=int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)
def p1(*args): ans = part1(*args); print(ans); return ans
def p2(*args): ans = part2(*args); print(ans); return ans

if not isfile(file_name):
	from aoc import get_input_file
	get_input_file(session_path=['..', '.env'])
# @formatter:on

from utils import *

data = parsefile(file_name,  [[[str], "\n"], "\n\n"])

prizes = []
for v in data:
	ax = int(v[0][2][2:-1])
	ay = int(v[0][3][2:])
	
	bx = int(v[1][2][2:-1])
	by = int(v[1][3][2:])
	
	tx = int(v[2][1][2:-1])
	ty = int(v[2][2][2:])
	
	prizes.append((ax, ay, bx, by, tx, ty))

def score(p):
	min_t = 10000000
	min_c = None
	
	for i in range(100+1):
		for j in range(100+1):
			cx = i * p[0] + j * p[2]
			cy = i * p[1] + j * p[3]
			
			if cx > p[4] or cy > p[5]:
				break
			
			if cx == p[4] and cy == p[5]:
				tc = i*3 + j
				
				if tc < min_t:
					#print(p, min_t, tc)
					min_t = tc
					min_c = (i, j)
					
					
	return min_t, min_c
		

def part1():
	t = 0
	
	for p in prizes:
		s = score(p)
		if s[1] is not None:
			t += s[0]
			
	return t

def score2(p):
	tx = p[4] + 10000000000000
	ty = p[5] + 10000000000000
	
	
	"""
	tx = i * ax + j * bx
	ty = i * ay + j * by
	
	i * ay = ty - (j * by)
	i = (ty - (j * by)) / ay
	
	tx = ((ty - (j * by)) / ay) * ax + j * bx
	tx = ty*ax - (j*by*ax)/ay + j*bx
	
	
	
	"""
	
	import sympy as sp
	
	i = sp.Symbol("i", real=True)
	j = sp.Symbol("j", real=True)
	
	e1 = sp.Eq(i * p[0] + j * p[2], tx)
	e2 = sp.Eq(i * p[1] + j * p[3], ty)
	
	r = sp.solve([e1, e2], (i, j))
	ri = r[i]
	rj = r[j]
	
	if isinstance(ri, sp.core.numbers.Integer) and isinstance(rj, sp.core.numbers.Integer):
		print(ri, rj, tx, ty)
		assert ri * p[0] + rj * p[2] == tx
		assert ri * p[1] + rj * p[3] == ty
		return ri * 3 + rj
	

def part2():
	t = 0
	
	for p in prizes:
		s = score2(p)
		if s is not None:
			t += s
			
	return t


p1()
p2()
