from os.path import isfile, join as path_join
from sys import path as sys_path
sys_path.insert(1, path_join(sys_path[0], '..'))
file_name = path_join('input', 'day17.txt')
def to_list(mf: object = int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]
def to_gen(mf: object = int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)
def p1(*args): ans = part1(*args); print(ans); return ans
def p2(*args): ans = part2(*args); print(ans); return ans

if not isfile(file_name):
	from aoc import get_input_file
	get_input_file(session_path=['..', '.env'])

from utils import parsefile

data = parsefile(file_name, [str, " "])

x_range = data[2].split("..")
x_range = int(x_range[0][2:]), int(x_range[1][:-1])

y_range = data[3].split("..")
y_range = int(y_range[0][2:]), int(y_range[1])

def calc_traj(xv, yv):
	ixv = xv
	iyv = yv
	max_height = 0
	
	cx, cy = 0, 0
	end_x = max(x_range)
	end_y = min(y_range)
	
	while cx <= end_x:
		cx += xv
		cy += yv
		
		if xv > 0:
			xv -= 1
		elif xv < 0:
			xv += 1
		yv -= 1
		#if ixv==7 and iyv==-1:print(cx, cy, xv, yv)
		max_height = max(max_height, cy)
		
		if min(x_range) <= cx <= max(x_range):
			if min(y_range) <= cy <= max(y_range):
				return True, max_height
	
		if yv < 0 and cy < min(y_range):
			break
	
	return False, max_height

def part1():
	max_height = 0
	max_traj = (-1000000, -1000000)
	
	for yv in range(-100, 100):
		for xv in range(1, max(x_range)+1):
			res = calc_traj(xv, yv)
			if res[0]:
				if res[1] > max_height:
					max_height = res[1]
					max_traj = (xv, yv)
					
	return max_height


def part2():
	hits = set()
	
	for yv in range(-100, 100):
		for xv in range(0, max(x_range)+1):
			res = calc_traj(xv, yv)
			if res[0]:
				hits.add((xv, yv))
		
	#print("ch", len(ch))
	#print(ch ^ hits)
	
	return len(hits)


p1()
p2()
