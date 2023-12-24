# @formatter:off
from os.path import isfile, join as path_join
from sys import path as sys_path
sys_path.insert(1, path_join(sys_path[0], '..'))
file_name = path_join('input', 'day24.txt')
def to_list(mf: object = int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]
def to_gen(mf: object = int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)
def p1(*args): ans = part1(*args); print(ans); return ans
def p2(*args): ans = part2(*args); print(ans); return ans

if not isfile(file_name):
	from aoc import get_input_file
	get_input_file(session_path=['..', '.env'])
# @formatter:on

from utils import *

data = parsefile(file_name,  [[[int, ","], "@"], "\n"])


xy_lines = []
for d in data:
	"""
	sx, sy | vx, vy
	
	y = mx + c
	m = vy / vx
	c = sy - m*sx
	"""
	
	m = d[1][1] / d[1][0]
	c = d[0][1] - m * d[0][0]
	
	xy_lines.append((m, c))

def collide(line1, line2):
	a1 = line1[0]
	b1 = -1
	c1 = line1[1]
	
	a2 = line2[0]
	b2 = -1
	c2 = line2[1]
	
	den = (a1*b2 - a2*b2)
	if den == 0:
		return None
	
	x = (b1*c2 - b2*c1) / den
	y = (a2*c1 - a1*c2) / den
	
	return x, y

from math import copysign

def future(d1, d2, pos):
	return \
		all([copysign(1, d1[1][i]) == copysign(1, pos[i] - d1[0][i]) for i in range(len(pos))]) and \
		all([copysign(1, d2[1][i]) == copysign(1, pos[i] - d2[0][i]) for i in range(len(pos))])

def part1():
	area = [200000000000000, 400000000000000]
	c = 0
	
	for i in range(len(data)):
		for j in range(i+1, len(data)):			
			r = collide(xy_lines[i], xy_lines[j])
			if r is not None:
				if future(data[i], data[j], r):
					if area[0] <= r[0] <= area[1] and area[0] <= r[1] <= area[1]:
						c += 1
				
	return c

import sympy as sp

def part2():
	x, y, z = sp.symbols("x, y, z")
	vx, vy, vz = sp.symbols("vx, vy vz")
	times = (tx, ty, tz) = sp.symbols("t0 t1 t2")
	
	eqs = []
	for i in range(3):
		line = data[i]
		
		ex = sp.Eq(line[0][0] + line[1][0] * times[i], x + vx * times[i])
		ey = sp.Eq(line[0][1] + line[1][1] * times[i], y + vy * times[i])
		ez = sp.Eq(line[0][2] + line[1][2] * times[i], z + vz * times[i])
		
		eqs.append(ex)
		eqs.append(ey)
		eqs.append(ez)
	
	res = sp.solve(eqs, (x, y, z, vx, vy, vz, tx, ty, tz))
	rx, ry, rz, rvx, rvy, rvz, rt0, rt1, rt2 = res[0]
	return rx + ry + rz


p1()
p2()
