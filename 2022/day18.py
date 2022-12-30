# @formatter:off
from os.path import isfile, join as path_join
from sys import path as sys_path
sys_path.insert(1, path_join(sys_path[0], '..'))
file_name = path_join('input', 'day18.txt')
def to_list(mf: object = int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]
def to_gen(mf: object = int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)
def p1(*args): ans = part1(*args); print(ans); return ans
def p2(*args): ans = part2(*args); print(ans); return ans

if not isfile(file_name):
	from aoc import get_input_file
	get_input_file(session_path=['..', '.env'])
# @formatter:on

from utils import parsefile

cubes = parsefile(file_name, [[int, ","], "\n"])

def count_sides(cube, cubes):
	sides = 0
	for c in cubes:
		if cube == c:
			continue
			
		diff = abs(cube[0] - c[0]) + abs(cube[1] - c[1]) + abs(cube[2] - c[2])
		if diff == 1:
			sides += 1
			
	return sides

def part1():
	area = 0
	for cube in cubes:
		area += 6 - count_sides(cube, cubes)
		
	return area

def bfs(min_xyz, max_xyz):
	found = set()
	
	to_check = set([min_xyz])
	while to_check:
		curr = list(to_check)[0]
		to_check.remove(curr)
		
		found.add(curr)
		
		for x in range(-1, 2):
			for y in range(-1, 2):
				for z in range(-1, 2):
					if x==0 and y==0 and z==0:
						continue
					if abs(x) + abs(y) + abs(z) != 1:
						continue
					
					np = (curr[0]+x, curr[1]+y, curr[2]+z)
					
					if np[0] >= min_xyz[0] and np[1] >= min_xyz[1] and np[2] >= min_xyz[2]:
						if np[0] <= max_xyz[0] and np[1] <= max_xyz[1] and np[2] <= max_xyz[2]:
							if np not in found:
								if list(np) not in cubes:
									#print(np)
									to_check.add(np)
		
	return found

def part2():
	min_xyz = [10000000, 10000000, 1000000]
	max_xyz = [0, 0, 0]
	
	for cube in cubes:
		for i in range(3):
			if cube[i] < min_xyz[i]:
				min_xyz[i] = cube[i]
			if cube[i] > max_xyz[i]:
				max_xyz[i] = cube[i]
	
	min_xyz = (min_xyz[0]-1, min_xyz[1]-1, min_xyz[2]-1)
	max_xyz = (max_xyz[0]+1, max_xyz[1]+1, max_xyz[2]+1)
	
	outside = bfs(min_xyz, max_xyz)
	
	sides = 0
	for cube in cubes:
		sides += count_sides(cube, outside)
		
	return sides


p1()
p2()
