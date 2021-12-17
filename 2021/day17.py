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

#x_range = 20, 30
#y_range = -10, -5

print(x_range)
print(y_range)

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

ch = [(int(v.split(",")[0]), int(v.split(",")[1])) for v in """23,-10  25,-9   27,-5   29,-6   22,-6   21,-7   9,0     27,-7   24,-5
25,-7   26,-6   25,-5   6,8     11,-2   20,-5   29,-10  6,3     28,-7
8,0     30,-6   29,-8   20,-10  6,7     6,4     6,1     14,-4   21,-6
26,-10  7,-1    7,7     8,-1    21,-9   6,2     20,-7   30,-10  14,-3
20,-8   13,-2   7,3     28,-8   29,-9   15,-3   22,-5   26,-8   25,-8
25,-6   15,-4   9,-2    15,-2   12,-2   28,-9   12,-3   24,-6   23,-7
25,-10  7,8     11,-3   26,-7   7,1     23,-9   6,0     22,-10  27,-6
8,1     22,-8   13,-4   7,6     28,-6   11,-4   12,-4   26,-9   7,4
24,-10  23,-8   30,-8   7,0     9,-1    10,-1   26,-5   22,-9   6,5
7,5     23,-6   28,-10  10,-2   11,-1   20,-9   14,-2   29,-7   13,-3
23,-5   24,-8   27,-9   30,-7   28,-5   21,-10  7,9     6,6     21,-5
27,-10  7,2     30,-9   21,-8   22,-7   24,-9   20,-6   6,9     29,-5
8,-2    27,-8   30,-5   24,-7""".replace("\n", " ").split()]

ch = set(ch)

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
