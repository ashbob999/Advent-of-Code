# @formatter:off
from os.path import isfile, join as path_join
from sys import path as sys_path
sys_path.insert(1, path_join(sys_path[0], '..'))
file_name = path_join('input', 'day22.txt')
def to_list(mf: object = int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]
def to_gen(mf: object = int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)
def p1(*args): ans = part1(*args); print(ans); return ans
def p2(*args): ans = part2(*args); print(ans); return ans

if not isfile(file_name):
	from aoc import get_input_file
	get_input_file(session_path=['..', '.env'])
# @formatter:on

from utils import *

data = parsefile(file_name,  [[[int, ","], "~"], "\n"])

# check only 1 axis differ
for d in data:
	xd = abs(d[0][0]-d[1][0])
	yd = abs(d[0][1]-d[1][1])
	zd = abs(d[0][2]-d[1][2])
	
	xd = 1 if xd > 0 else 0
	yd = 1 if yd > 0 else 0
	zd = 1 if zd > 0 else 0
	delta = xd+yd+zd
	assert delta <= 1, print(d)

# sort by lowest z value
blocks_ = [[sorted([d[0][0], d[1][0]]), sorted([d[0][1], d[1][1]]), sorted([d[0][2], d[1][2]])] for d in data]
blocks_ = sorted(blocks_, key=lambda x: x[2][0])

from copy import deepcopy
blocks = deepcopy(blocks_)

def overlap(r1, r2):
	if r1[0] > r2[0]:
		r1, r2 = r2, r1
	
	if r1[1] < r2[0]:
		return False
	else:
		return True
		
assert overlap([0, 5], [10, 20]) == False
assert overlap([0, 5], [3, 20]) == True
assert overlap([0, 5], [5, 20]) == True
assert overlap([12, 13], [3, 20]) == True

def collide(z, xr, yr, blocks):
	for i in range(len(blocks)):
		block = blocks[i]
		if block[2][0] > z:
			return False
		if block[2][0] <= z <= block[2][1]:
			if overlap(xr, block[0]) and overlap(yr, block[1]):
				return True
		
	return False

assert collide(1, (1,1), (3,3), [((1,1), (3,3), (1,1))]) == True
assert collide(2, (0, 2), (0, 0), [((0, 2), (2, 2), (2, 2))]) == False

def fall(block, blocks):
	prev_block = deepcopy(block)
	while block[2][0] > 1:
		prev_block = block
		block = [block[0], block[1], [block[2][0]-1, block[2][1]-1]]
		if collide(block[2][0], block[0], block[1], blocks):
			return prev_block
			
	return block

assert fall([[1,1], [3,3], [2,2]], []) == [[1,1], [3,3], [1,1]]
assert fall([[1,1], [3,3], [10,20]], []) == [[1,1], [3,3], [1,11]]
assert fall([[1,1], [3,3], [10,20]], [((1,1), (3,3), (1,1))]) == [[1,1], [3,3], [2,12]]

from bisect import insort

fallen_blocks = []
for block in blocks:
	b = fall(block, fallen_blocks)
	# insort(fallen_blocks, b, key=lambda x: x[2][0])
	fallen_blocks.append(b)
	fallen_blocks = sorted(fallen_blocks, key=lambda x: x[2][0])


def collide2(z, xr, yr, blocks):
	colls = []
	for i in range(len(blocks)):
		block = blocks[i]
		if block[2][0] > z:
			return colls
		if block[2][0] <= z <= block[2][1]:
			if overlap(xr, block[0]) and overlap(yr, block[1]):
				colls.append(i)
		
	return colls

# gen dependency map
above = {}
below = {}

for i in range(len(fallen_blocks)):
	block = fallen_blocks[i]
	colls = collide2(block[2][0]-1, block[0], block[1], fallen_blocks)
	below[i] = colls[:]
	for c in colls:
		if c not in above:
			above[c] = []
		above[c].append(i)


def part1():
	t = 0
	
	# count all with no above
	# count all where all above have mutiple below
	for i in range(len(fallen_blocks)):
		if i in above:
			if len(above[i]) == 0:
				t += 1
			res = True
			for v in above[i]:
				if v in below and len(below[v]) > 1:
					pass
				else:
					res = False
			if res:
				t += 1
		else:
			t += 1
			
	return t


def chain(above, below, i):
	if i not in above:
		return 0
	c = 0
	# remove all i
	for k, v in below.items():
		if i in v:
			v.remove(i)
			if len(v) == 0:
				c += 1
				c += chain(above, below, k)
				
	return c

"""
import pydot

graph = pydot.Dot(graph_type="digraph")
nodes = [pydot.Node(str(i)) for i in range(len(fallen_blocks))]
for n in nodes:
	graph.add_node(n)
for k, v in below.items():
	for vv in v:
		edge = pydot.Edge(nodes[vv], nodes[k])
		graph.add_edge(edge)
graph.write_png("day22_output.png")
graph.write_svg("day22_output.svg")
"""

def part2():
	global below, above
	
	t = 0
	for i in range(len(fallen_blocks)):
		above_ = deepcopy(above)
		below_ = deepcopy(below)
		r = chain(above_, below_, i)
		#print(i, r)
		t += r
		
	return t


p1()
p2()
