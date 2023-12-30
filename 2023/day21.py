# @formatter:off
from os.path import isfile, join as path_join
from sys import path as sys_path
sys_path.insert(1, path_join(sys_path[0], '..'))
file_name = path_join('input', 'day21.txt')
def to_list(mf: object = int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]
def to_gen(mf: object = int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)
def p1(*args): ans = part1(*args); print(ans); return ans
def p2(*args): ans = part2(*args); print(ans); return ans

if not isfile(file_name):
	from aoc import get_input_file
	get_input_file(session_path=['..', '.env'])
# @formatter:on

from utils import *

data = parsefile(file_name,  [list, "\n"])

input = """...........
.....###.#.
.###.##..#.
..#.#...#..
....#.#....
.##..S####.
.##..#...#.
.......##..
.##.#.####.
.##..##.##.
..........."""
input_ = """.................................
.....###.#......###.#......###.#.
.###.##..#..###.##..#..###.##..#.
..#.#...#....#.#...#....#.#...#..
....#.#........#.#........#.#....
.##...####..##...####..##...####.
.##..#...#..##..#...#..##..#...#.
.......##.........##.........##..
.##.#.####..##.#.####..##.#.####.
.##..##.##..##..##.##..##..##.##.
.................................
.................................
.....###.#......###.#......###.#.
.###.##..#..###.##..#..###.##..#.
..#.#...#....#.#...#....#.#...#..
....#.#........#.#........#.#....
.##...####..##..S####..##...####.
.##..#...#..##..#...#..##..#...#.
.......##.........##.........##..
.##.#.####..##.#.####..##.#.####.
.##..##.##..##..##.##..##..##.##.
.................................
.................................
.....###.#......###.#......###.#.
.###.##..#..###.##..#..###.##..#.
..#.#...#....#.#...#....#.#...#..
....#.#........#.#........#.#....
.##...####..##...####..##...####.
.##..#...#..##..#...#..##..#...#.
.......##.........##.........##..
.##.#.####..##.#.####..##.#.####.
.##..##.##..##..##.##..##..##.##.
................................."""
#data = parse(input, [list, "\n"])

height = len(data)
width = len(data[0])
print(width, height)

start = None
for y in range(height):
	for x in range(width):
		if data[y][x] == "S":
			start = (x, y)
			break
	if start:
		break

adj = ((0, 1), (0, -1), (1, 0), (-1, 0))

grid = [r[:] for r in data]

def step(gardens):
	next_gardens = set()
	
	for g in gardens:
		for ad in adj:
			nx = g[0] + ad[0]
			ny = g[1] + ad[1]
			
			if 0 <= nx < width and 0 <= ny < height:
				#print(nx, ny, width, height)
				if grid[ny][nx] != "#":
					next_gardens.add((nx, ny))
	
	return next_gardens
	
def step2(gardens):
	next_gardens = set()
	
	for g in gardens:
		for ad in adj:
			nx = g[0] + ad[0]
			ny = g[1] + ad[1]
			
			nxm = nx % width
			nym = ny % height
			
			#print(nx, ny, width, height)
			if grid[nym][nxm] != "#":
				next_gardens.add((nx, ny))
	
	return next_gardens

def part1():
	gardens = set()
	gardens.add(start)
	
	vals = []
	
	for i in range(250):
		gardens = step2(gardens)
		vals.append(len(gardens))
		print(i, vals[-1])
	
	g = [r[:] for r in grid]
	for garden in gardens:
		if g[garden[1]%height][garden[0]%width] ==".":
			g[garden[1]%height][garden[0]%width] = "O"
	
	"""
	with open("day21_output.txt", "w") as f:
		for r in g:
			f.write("".join(r))
			f.write("\n")
	"""
	
	d1 = [vals[i] - vals[i-1] for i in range(1, len(vals))]
	d2 = [d1[i] - d1[i-1] for i in range(1, len(d1))]
	d3 = [d2[i] - d2[i-1] for i in range(1, len(d2))]
	d4 = [d3[i] - d3[i-1] for i in range(1, len(d3))]
	
	
	print(d1)
	print(d2)
	print(d3)
	print(d4)
	return len(gardens)

# initial caching
cache = {}


def check(start):
	even = {}
	odd = {}
	
	max_v = (start, 0)
	min_top = None
	min_bottom = None
	min_left = None
	min_right = None
	
	if grid[start[1]][start[0]] == "#":
		assert False
		return None
	
	to_check = [(start, 0)]
	to_check_set = set()
	to_check_set.add(start)
	while len(to_check) > 0:
		#print(len(to_check), to_check)
		if len(to_check) > 10:
			pass#quit()
		curr, dist = to_check.pop(0)
		to_check_set.remove(curr)
		
		if dist > max_v[1]:
			max_v = (curr, dist)
		
		if dist % 2 == 0:
			even[curr] = dist
		else:
			odd[curr] = dist
		
		if curr[0] == 0: # left
			if min_left is None:
				min_left = (curr, dist)
				
		if curr[0] == width-1: # right
			if min_right is None:
				min_right = (curr, dist)
				
		if curr[1] == 0: # top
			if min_top is None:
				min_top = (curr, dist)
		
		if curr[1] == height-1: # bottom
			if min_bottom is None:
				min_bottom = (curr, dist)
		
		for ad in adj:
			nx = curr[0] + ad[0]
			ny = curr[1] + ad[1]
			
			if 0 <= nx < width and 0 <= ny < height:
				#print(nx, ny, width, height)
				if grid[ny][nx] != "#":
					p = (nx, ny)
					if p not in odd and p not in even:
						if p not in to_check_set:
							to_check.append((p, dist+1))
							to_check_set.add(p)

	assert min_left is not None
	assert min_right is not None
	assert min_top is not None
	assert min_bottom is not None
	
	return odd, even, (min_left, min_right, min_top, min_bottom), max_v

"""
# top
for x in range(width):
	p = (x, 0)
	print(p)
	if p not in cache:
		cache[p] = check(p)
print("top done")
		
# bottom
for x in range(width):
	p = (x, height-1)
	print(p)
	if p not in cache:
		cache[p] = check(p)
print("bottom done")
		
# left
for y in range(height):
	p = (0, y)
	print(p)
	if p not in cache:
		cache[p] = check(p)
print("left done")
		
# right
for y in range(height):
	p = (width-1, y)
	print(p)
	if p not in cache:
		cache[p] = check(p)
print("right done")
"""


def solve(steps, start):
	even = steps %2==0
	
	seen = set()
	
	to_check = []
	#to_check_set = set()
	to_check_data = {}
	
	to_check.append((0, 0))
	to_check_data[(0, 0)] = (start, 0)
	
	total = 0
	
	while len(to_check) > 0:
		curr = to_check.pop(0)
		#to_check_set.remove(curr)
		entry, curr_step = to_check_data[curr]
		del to_check_data[curr]
		
		if curr in seen:
			continue
			
		seen.add(curr)
		
		odd, even, exits, max_v = check(entry)
		print(curr, entry, exits)
		
		print("-", curr, curr_step, max_v, steps)
		# check if no more grids need to be checked
		if curr_step + max_v[1] >= steps:
			diff = steps - curr_step
			# ee = e
			# oo = e
			# eo = o
			# oe = o
			curr_even = curr_step%2==0
			if curr_even and even:
				vals = even # even
			else:
				vals = odd # odd
			
			t= 0
			print("add1 check", diff)
			for k, v in vals.items():
				if v <= diff:
					print(k, v)
					t += 1
			
			print("adding 1:", curr, t)
			total += t
		
		elif curr_step + max_v[1] < steps:
			curr_even = curr_step%2==0
			if curr_even and even:
				vals = even # even
			else:
				vals = odd # odd
			
			print("adding 2: ", curr, len(vals))
			total += len(vals)
		else:
			assert False
		
		for i, exit in enumerate(exits):
			if curr_step + exit[1] < steps:
				if i == 0: # left
					next_ = (curr[0]-1, curr[1])
					np = (width-1, exit[0][1])
				elif i == 1: # right
					next_ = (curr[0]+1, curr[1])
					np = (0, exit[0][1])
				elif i == 2: # top
					next_ = (curr[0], curr[1]-1)
					np = (exit[0][0], height-1)
				elif i == 3: # bottom
					next_ = (curr[0], curr[1]+1)
					np = (exit[0][0], 0)
				else:
					assert False
				
				next_steps = curr_step + exit[1] + 1
				#print("next", next_, exit, np, next_steps)
				if next_ not in to_check_data:
					to_check.append(next_)
					to_check_data[next_] = (np, next_steps)
				if to_check_data[next_][1] > next_steps:
					to_check_data[next_] = (np, next_steps)
					
	print("seen", steps, seen)
	return total



def part2():
	step_count = 26501365
	
	r = solve(step_count, start)
	return r


p1()
print()

test_values = [
	(6, 16),
	(10, 50),
	(50, 1594),
	(100, 6536),
	(500, 167004),
	(1000, 668697),
	(5000, 16733044)
]


for v in test_values:
	print()
	r = solve(v[0], start)
	assert v[1] == r, print(v, r)

p2()
