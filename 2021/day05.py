from os.path import isfile, join as path_join
from sys import path as sys_path
sys_path.insert(1, path_join(sys_path[0], '..'))
file_name = path_join('input', 'day05.txt')
def to_list(mf: object = int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]
def to_gen(mf: object = int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)
def p1(*args): ans = part1(*args); print(ans); return ans
def p2(*args): ans = part2(*args); print(ans); return ans

if not isfile(file_name):
	from aoc import get_input_file
	get_input_file(session_path=['..', '.env'])

from utils import parsefile

data = parsefile(file_name, [[[int, ","], 1, None, [int, ","]], "\n"])


def part1():
	points = {}
	
	for line in data:
		x1 = min(line[0][0], line[1][0])
		x2 = max(line[0][0], line[1][0])
		y1 = min(line[0][1], line[1][1])
		y2 = max(line[0][1], line[1][1])
		
		if x1 == x2:
			for y in range(y1, y2+1):
				point = (x1, y)
				if point in points:
					points[point] += 1
				else:
					points[point] = 1
			
		elif y1 == y2:
			for x in range(x1, x2+1):
				point = (x, y1)
				if point in points:
					points[point] += 1
				else:
					points[point] = 1
		else:
			continue
			
			
	return len(list(filter(lambda x: x >=2, points.values())))


def part2():
	points = {}
	
	for line in data:
		x1 = min(line[0][0], line[1][0])
		x2 = max(line[0][0], line[1][0])
		y1 = min(line[0][1], line[1][1])
		y2 = max(line[0][1], line[1][1])
		
		if x1 == x2:
			for y in range(y1, y2+1):
				point = (x1, y)
				if point in points:
					points[point] += 1
				else:
					points[point] = 1
			
		elif y1 == y2:
			for x in range(x1, x2+1):
				point = (x, y1)
				if point in points:
					points[point] += 1
				else:
					points[point] = 1
		else:
			x1 = line[0][0]
			x2 = line[1][0]
			y1 = line[0][1]
			y2 = line[1][1]
			dx = 1 if x2 > x1 else -1
			dy = 1 if y2 > y1 else -1
			for step in range(0, abs(x2-x1)+1, 1):
				point = (x1+dx*step, y1+dy*step)
				if point in points:
					points[point] += 1
				else:
					points[point] = 1
			
	return len(list(filter(lambda x: x >=2, points.values())))


p1()
p2()
