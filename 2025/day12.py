# @formatter:off
from os.path import isfile, join as path_join
from sys import path as sys_path
sys_path.insert(1, path_join(sys_path[0], '..'))
file_name = path_join('input', 'day12.txt')
def to_list(mf=int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]
def to_gen(mf=int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)
def p1(*args): ans = part1(*args); print(ans); return ans
def p2(*args): ans = part2(*args); print(ans); return ans

if not isfile(file_name):
	from aoc import get_input_file
	get_input_file(session_path=['..', '.env'])
# @formatter:on

from utils import *

data = parsefile(file_name, "\n\n")

presents = []

def gts(g, w, h):
	s = set()
	for y in range(h):
		for x in range(h):
			if g[y][x] == "#":
				s.add((x, y))
	return frozenset(s)



def flip(tile, dir):
	if dir == 0:
		return [tile[i] for i in range(len(tile) - 1, -1, -1)]
	elif dir == 1:
		return [t[::-1] for t in tile]


def transpose(tile):
	return ["".join(x) for x in zip(*tile)]


def rotate(tile, dir):
	if dir == 0:
		return tile
	if dir == 90:
		tile = transpose(tile)
		return flip(tile, 1)

for v in data[:-1]:
	ps = v.split("\n")
	idx = int(ps[0][:-1])
	
	w = len(ps[1])
	h = len(ps) - 1

	vars = set()

	ga = ps[1:]
	g_ = gts(ga, w, h)
	size = len(g_)
	
	vars.add(g_)
	vars.add(gts(flip(ga, 0), w, h))
	vars.add(gts(flip(ga, 1), w, h))
	
	for i in range(3):
		ga = rotate(ga, 90)
		
		vars.add(gts(ga, w, h))
		vars.add(gts(flip(ga, 0), w, h))
		vars.add(gts(flip(ga, 1), w, h))
	
	presents.insert(idx, (w, h, size, vars))


grids = []
for v in data[-1].split("\n"):
	ps = v.split()
	
	wh = ps[0][:-1].split("x")
	w = int(wh[0])
	h = int(wh[1])
	
	counts = list(map(int, ps[1:]))
	
	grids.append((w, h, counts))


fg = []
for g in grids:
	ta = g[0] * g[1]
	na = sum([g[2][i] * presents[i][2] for i in range(len(g[2]))])

	if na <= ta:
		fg.append(g)

print(len(grids), len(fg))

# this problem is silly,ifor the real input
# we dont even neeed tocaclulate how they fit together
# just that theres enough space to fitthenm all in
# Note that thisndoes not apply to the example input

def part1():
	return len(fg)


def part2():
	pass


p1()
p2()
