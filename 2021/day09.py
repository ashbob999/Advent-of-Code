from os.path import isfile, join as path_join
from sys import path as sys_path
sys_path.insert(1, path_join(sys_path[0], '..'))
file_name = path_join('input', 'day09.txt')
def to_list(mf: object = int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]
def to_gen(mf: object = int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)
def p1(*args): ans = part1(*args); print(ans); return ans
def p2(*args): ans = part2(*args); print(ans); return ans

if not isfile(file_name):
	from aoc import get_input_file
	get_input_file(session_path=['..', '.env'])

from utils import parsefile

data = parsefile(file_name, [list, "\n"])

heights = [[int(v) for v in r] for r in data]

w = len(heights[0])
h = len(heights)

adj = [(0, 1), (0, -1), (1, 0), (-1, 0)]

def check_adj(x, y):
	lc = 0
	ac = 0
	for a in adj:
		nx = x + a[0]
		ny = y + a[1]
		
		if nx >= 0 and nx < w and ny >= 0 and ny < h:
			ac += 1
			if heights[y][x] < heights[ny][nx]:
				lc += 1
				
	return lc == ac
		

low_points = []

def part1():
	s = 0
	for y in range(h):
		for x in range(w):
			lower = check_adj(x, y)
			if lower:
				low_points.append((x, y))
				s += 1 + heights[y][x]
				
	return s

def get_adj(x, y):
	ad = []
	for a in adj:
		nx = x + a[0]
		ny = y + a[1]
		
		if nx >= 0 and nx < w and ny >= 0 and ny < h:
			ad.append((nx, ny))
			
	return ad

def get_basin(x, y):
	basin = set([(x, y)])
	
	to_check = set([(x, y)])
	checked = set()
	
	while len(to_check) > 0:
		cp = list(to_check)[0]
		to_check.remove(cp)
		checked.add(cp)
		
		level = heights[cp[1]][cp[0]]
		
		for np in get_adj(cp[0], cp[1]):
			if np not in checked:
				n_level = heights[np[1]][np[0]]
				if n_level > level and n_level < 9:
					basin.add(np)
					to_check.add(np)
	
	return basin

def part2():
	basins = []
	
	for lp in low_points:
		basins.append(get_basin(lp[0], lp[1]))

	basins = sorted(basins, key=len, reverse=True)
	
	p = 1
	for b in basins[:3]:
		p *= len(b)
		
	return p

p1()
p2()
