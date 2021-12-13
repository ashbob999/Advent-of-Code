from os.path import isfile, join as path_join
from sys import path as sys_path
sys_path.insert(1, path_join(sys_path[0], '..'))
file_name = path_join('input', 'day13.txt')
def to_list(mf: object = int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]
def to_gen(mf: object = int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)
def p1(*args): ans = part1(*args); print(ans); return ans
def p2(*args): ans = part2(*args); print(ans); return ans

if not isfile(file_name):
	from aoc import get_input_file
	get_input_file(session_path=['..', '.env'])

from utils import parsefile, parse

points, folds = parsefile(file_name, [[[int, ","], "\n"], 1, [[None, 2, [str, 1, int, "="]], "\n"], "\n\n"])
raw = """6,10
0,14
9,10
0,3
10,4
4,11
6,0
6,12
4,1
0,13
10,12
3,4
3,0
8,4
1,10
2,14
8,10
9,0

fold along y=7
fold along x=5"""
#points, folds =parse(raw, [[[int, ","], "\n"], 1, [[None, 2, [str, 1, int, "="]], "\n"], "\n\n"])

for i in range(len(folds)):
	folds[i] = folds[i][0]

grid = set()

for p in points:
	grid.add(tuple(p))

def part1():
	g = grid.copy()
	
	for fold in folds[:1]:
		line = fold[1]
		
		new_g = g.copy()
		
		if fold[0] == "y": # fold up
			for p in g:
				if p[1] > line:
					new_g.remove(p)
					new_g.add((p[0], p[1] - (p[1] - line)*2))
		else: # fold left
			for p in g:
				if p[0] > line:
					new_g.remove(p)
					new_g.add((p[0] - (p[0] - line)*2, p[1]))

		g = new_g
		
	return len(g)

def part2():
	g = grid.copy()
	
	for fold in folds:
		line = fold[1]
		
		new_g = g.copy()
		
		if fold[0] == "y": # fold up
			for p in g:
				if p[1] > line:
					new_g.remove(p)
					new_g.add((p[0], p[1] - (p[1] - line)*2))
		else: # fold left
			for p in g:
				if p[0] > line:
					new_g.remove(p)
					new_g.add((p[0] - (p[0] - line)*2, p[1]))

		g = new_g
	
	max_x = max(map(lambda p: p[0], g))
	max_y = max(map(lambda p: p[1], g))
	
	sg = [[" " for w in range(max_x+1)] for y in range(max_y+1)]
	
	for p in g:
		sg[p[1]][p[0]] = "#"
		
	for r in sg:
		print("".join(r))


p1()
p2()
