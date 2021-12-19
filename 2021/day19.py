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

from utils import parsefile, parse

data = parsefile(file_name, [[[None, 2, int, 1, " "], 1, [int, ","], 0, "\n"], "\n\n"])

scanners = {}
for d in data:
	id = d[0][0]
	s = set()
	for p in d[1:]:
		s.add(tuple(p))
		
	scanners[id] = sorted(s)

rots = [
{"x":(0, 1), "y":(1, 1), "z":(2, 1)},#1
{"x":(0, -1), "y":(1, -1), "z":(2, 1)},#2
{"x":(0, -1), "y":(1, 1), "z":(2, -1)},#3
{"x":(0, 1), "y":(1, -1), "z":(2, -1)},#4
{"x":(2, 1), "y":(0, 1), "z":(1, 1)},#5
{"x":(2, -1), "y":(0, -1), "z":(1, 1)},#6
{"x":(2, -1), "y":(0, 1), "z":(1, -1)},#7
{"x":(2, 1), "y":(0, -1), "z":(1, -1)},#8
{"x":(1, 1), "y":(2, 1), "z":(0, 1)},#9
{"x":(1, -1), "y":(2, -1), "z":(0, 1)},#10
{"x":(1, -1), "y":(2, 1), "z":(0, -1)},#11
{"x":(1, 1), "y":(2, -1), "z":(0, -1)},#12
{"x":(0, 1), "y":(2, -1), "z":(1, 1)},#13
{"x":(0, 1), "y":(2, 1), "z":(1, -1)},#14
{"x":(0, -1), "y":(2, 1), "z":(1, 1)},#15
{"x":(0, -1), "y":(2, -1), "z":(1, -1)},#16
{"x":(1, 1), "y":(0, 1), "z":(2, -1)},#17
{"x":(1, -1), "y":(0, 1), "z":(2, 1)},#18
{"x":(1, 1), "y":(0, -1), "z":(2, 1)},#19
{"x":(1, -1), "y":(0, -1), "z":(2, -1)},#20
{"x":(2, -1), "y":(1, 1), "z":(0, 1)},#21
{"x":(2, 1), "y":(1, -1), "z":(0, 1)},#22
{"x":(2, 1), "y":(1, 1), "z":(0, -1)},#23
{"x":(2, -1), "y":(1, -1), "z":(0, -1)},#24
]

found_rots = {0:rots[0]}

points = set([p for p in scanners[0]])

scanner_pos = {0:(0, 0, 0)}
rel_0_points = {0:scanners[0]}

def translate(points, rot):
	new_points = []
	
	for p in points:
		nx = p[rot["x"][0]] * rot["x"][1]
		ny = p[rot["y"][0]] * rot["y"][1]
		nz = p[rot["z"][0]] * rot["z"][1]
		
		new_points.append((nx, ny, nz))
		
	return new_points
		
def get_12_offsets(p1_points, p2_points):
	offsets = {}
	for p_a in p1_points:
		for p_b in p2_points:
			offset = (p_b[0]-p_a[0], p_b[1]-p_a[1], p_b[2]-p_a[2])
			if offset in offsets:
				offsets[offset] += 1
				if offsets[offset] >= 12:
					return  True, offset
			else:
				offsets[offset] = 1
				
	return False, None

def check_match(p1, p2, p1_rot):
	p1_points = rel_0_points[p1]
	
	for rot in rots:
		p2_points = translate(scanners[p2], rot)
		
		# find most common offest between p1 and p2 points
		has12, best_offset = get_12_offsets(p1_points, p2_points)
		if has12:
			return True, p2_points, best_offset
			
	return False, None, None

def find_pairs(rem_ids):
	for p1 in found_rots.keys():
		for p2 in rem_ids:
			res = check_match(p1, p2, found_rots[p1])
			if res[0]:
				scanner_pos[p2] = (-res[2][0], -res[2][1], -res[2][2])
				found_rots[p2] = res[1]
				rel_0_points[p2] = []
				for p in res[1]:
					np = (p[0]-res[2][0], p[1]-res[2][1], p[2]-res[2][2])
					points.add(np)
					rel_0_points[p2].append(np)
				return p1, p2
				
	return None, None

def find_all_pairs():
	rem_ids = set(scanners.keys())
	rem_ids.remove(0)
	
	while len(found_rots) < len(scanners):
		p1, p2 = find_pairs(rem_ids)
		rem_ids.discard(p2)
		print(rem_ids)

def part1():
	find_all_pairs()
	return len(points)


def part2():
	max_dist = 0
	for s1 in scanner_pos.keys():
		for s2 in scanner_pos.keys():
			if s1 == s2:
				continue
				
			p1 = scanner_pos[s1]
			p2 = scanner_pos[s2]
			
			dist = abs(p1[0]-p2[0]) + abs(p1[1]-p2[1]) + abs(p1[2]-p2[2])
			max_dist = max(max_dist, dist)
			
	return max_dist

p1()
p2()
