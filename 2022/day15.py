# @formatter:off
from os.path import isfile, join as path_join
from sys import path as sys_path
sys_path.insert(1, path_join(sys_path[0], '..'))
file_name = path_join('input', 'day15.txt')
def to_list(mf: object = int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]
def to_gen(mf: object = int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)
def p1(*args): ans = part1(*args); print(ans); return ans
def p2(*args): ans = part2(*args); print(ans); return ans

if not isfile(file_name):
	from aoc import get_input_file
	get_input_file(session_path=['..', '.env'])
# @formatter:on

from utils import parsefile, parse

data = parsefile(file_name, [[" "], "\n"])

rd = """Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3"""
dataa = parse(rd, [[" "], "\n"])

sensors = {}
beacons = set()

for line in data:
	sx = int(line[2][2:-1])
	sy = int(line[3][2:-1])
	
	bx = int(line[8][2:-1])
	by = int(line[9][2:])
	
	dist = abs(sx-bx) + abs(sy-by)
	sensors[(sx, sy)] = (bx, by, dist)
	beacons.add((bx, by))

"""
cannot = set()
print(len(sensors))
i=0
for sensor, beacon in sensors.items():
	print(i)
	i+=1
	dist = beacon[2]
	print(dist)
	for y in range(dist+1):
		minx = sensor[0] - (dist - y)
		maxx = sensor[0] + (dist - y)
		cannot.add(((minx, maxx), y))
"""

def part1():
	y = 2000000
	
	minx = 1000000000
	maxx = 0
	
	cannot = set()
	
	for sensor, beacon in sensors.items():
		dist = beacon[2]
		if abs(sensor[1] - y) <= dist:
			excess = dist - abs(sensor[1] - y)
			for x in range(-excess, excess+1):
				xp = sensor[0] + x
				if (xp, y) not in beacons:
					cannot.add(sensor[0] + x)
	
	#print(cannot)
	return len(cannot)


def part2():
	minv = 0
	maxv = 4000000
	
	
	sens = list(sensors.keys())
	sens = sorted(sens, key=lambda x: x[0])
	
	print()
	for y in range(maxv+1):
		if y % 50000 ==0: print("y", y)
		x=0
		
		for sen in sens:
			dist = sensors[sen][2]
			test_dist = dist - abs(y-sen[1])
			
			if abs(x - sen[0]) <= test_dist:
				x = sen[0] + test_dist +1
				
		if x <= maxv:
			print(x, y)
			return x * 4000000 + y
		

#p1()
p2()
