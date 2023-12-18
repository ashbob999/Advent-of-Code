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

from utils import *

data = parsefile(file_name,  [[str, 1, int, 1, str], "\n"])

dirs = {
	"L": (-1, 0),
	"R": (1, 0),
	"U": (0, -1),
	"D": (0, 1)
}


# shoelace formula
def polygonArea(polygon):
	# Initialize area
	area = 0.0
	
	# Calculate value of shoelace formula
	j = len(polygon) - 1
	for i in range(0,len(polygon)):
		area += (polygon[j][0] + polygon[i][0]) * (polygon[j][1] - polygon[i][1])
		j = i # j is previous vertex to i
	
	# Return absolute value
	return int(abs(area / 2.0))
	

def part1():
	path = []
	start = (0, 0)
	curr = start
	path.append(curr)
	
	boundary = 0
	
	for d in data:
		dir = dirs[d[0]]
		amnt = d[1]
			
		boundary += amnt
		
		curr = (curr[0] + amnt * dir[0], curr[1] + amnt * dir[1])
		path.append(curr)
	
	area = polygonArea(path)
	
	# picks theoreom
	res = area + (boundary//2) + 1
	return res


def part2():
	path = []
	start = (0, 0)
	curr = start
	path.append(curr)
	
	boundary = 0
	
	for d in data:
		rgb = d[2][2:-1]
		
		dir_num = int(rgb[-1], 16)
		if dir_num == 0:
			dir = dirs["R"]
		elif dir_num == 1:
			dir = dirs["D"]
		elif dir_num == 2:
			dir = dirs["L"]
		elif dir_num == 3:
			dir = dirs["U"]
		else:
			assert False
		
		amnt = int(rgb[:5], 16)
		
		boundary += amnt
		
		curr = (curr[0] + amnt * dir[0], curr[1] + amnt * dir[1])
		path.append(curr)
	
	area = polygonArea(path)
	
	# picks theoreom
	res = area + (boundary//2) + 1
	return res


p1()
p2()
