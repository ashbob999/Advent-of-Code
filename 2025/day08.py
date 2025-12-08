# @formatter:off
from os.path import isfile, join as path_join
from sys import path as sys_path
sys_path.insert(1, path_join(sys_path[0], '..'))
file_name = path_join('input', 'day08.txt')
def to_list(mf=int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]
def to_gen(mf=int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)
def p1(*args): ans = part1(*args); print(ans); return ans
def p2(*args): ans = part2(*args); print(ans); return ans

if not isfile(file_name):
	from aoc import get_input_file
	get_input_file(session_path=['..', '.env'])
# @formatter:on

from utils import *

data = parsefile(file_name, [[int, ","], "\n"])
cc = 1000


def dist(a, b):
	return sum((b[i] - a[i])**2 for i in range(len(a))) ** 0.5


joins = []
for i in range(len(data)):
	for j in range(i+1, len(data)):
		if i == j:
			continue
		
		a = tuple(data[i])
		b = tuple(data[j])
		d = dist(a, b)
		joins.append((a, b, d))

joins = sorted(joins, key=lambda x: x[2])



def part1():
	js = joins[:cc]
	conns = []
	
	while len(js) > 0:
		added = False
		for i in range(len(js)):
			j = js[i]
			for v in conns:
				if j[0] in v:
					v.add(j[1])
					js.pop(i)
					added = True
					break
					
				if j[1] in v:
					v.add(j[0])
					js.pop(i)
					added = True
					break
					
			if added:
				break
		
		if not added:
			conns.append(set([js[0][0], js[0][1]]))
			js.pop(0)

	
	conns = sorted(conns, key=lambda x: len(x), reverse=True)
	return len(conns[0]) * len(conns[1]) * len(conns[2])
	


def part2():
	js = joins[:]
	conns = []
	
	lj1 = None
	
	for j_ in js:
		added = False
		for v in conns:
			if j_[0] in v:
				v.add(j_[1])
				added = True
				break
			elif j_[1] in v:
				v.add(j_[0])
				added = True
				break
		
		if not added:
			conns.append(set([j_[0], j_[1]]))
		else:
			didmerge = False
			i = 0
			while i < len(conns):
				for j in range(i+1, len(conns)):
					a = conns[i]
					b = conns[j]
					match = a & b
					if len(match) > 0:
						a |= b
						conns.pop(j)
						i -= 1
						didmerge = True
						break
				
				i+= 1

		if len(conns) == 1 and len(conns[0]) == len(data):
			lj1 = j_
			break

	return lj1[0][0] * lj1[1][0]


p1()
p2()
