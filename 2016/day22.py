# @formatter:off
from os.path import isfile, join as path_join
from sys import path as sys_path
sys_path.insert(1, path_join(sys_path[0], '..'))
file_name = path_join('input', 'day22.txt')
def to_list(mf: object = int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]
def to_gen(mf: object = int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)
def p1(*args): ans = part1(*args); print(ans); return ans
def p2(*args): ans = part2(*args); print(ans); return ans

if not isfile(file_name):
	from aoc import get_input_file
	get_input_file()
# @formatter:on

from utils import parsefile

raw_nodes = parsefile(file_name, [None, 2, [str], 0, "\n"])

nodes = {}

max_x = 0
max_y = 0

for n in raw_nodes:
	raw_pos = n[0].split("/")[-1].split("-")
	x = int(raw_pos[1][1:])
	y = int(raw_pos[2][1:])

	size = int(n[1][:-1])
	used = int(n[2][:-1])
	avail = int(n[3][:-1])
	percent = int(n[4][:-1])

	max_x = max(max_x, x)
	max_y = max(max_y, y)

	nodes[(x, y)] = (size, used, avail, percent)


def part1():
	pair_count = 0
	for node1 in nodes:
		node1_data = nodes[node1]
		for node2 in nodes:
			node2_data = nodes[node2]
			if node1 != node2 and 0 < node1_data[1] <= node2_data[2]:
				pair_count += 1

	return pair_count


def bfs(start, end, grid, walls, ingore_pos):
	w = len(grid[0])
	h = len(grid)
	to_check = [start]

	dists = {start: 0}

	while len(to_check) > 0:
		curr_pos = to_check.pop(0)
		curr_dist = dists[curr_pos]

		adj = []
		for y in range(-1, 2, 2):
			new_pos = (curr_pos[0], curr_pos[1] + y)
			if 0 <= new_pos[1] < h and grid[new_pos[1]][new_pos[0]] not in walls and new_pos not in ingore_pos:
				adj.append(new_pos)

		for x in range(-1, 2, 2):
			new_pos = (curr_pos[0] + x, curr_pos[1])
			if 0 <= new_pos[0] < w and grid[new_pos[1]][new_pos[0]] not in walls and new_pos not in ingore_pos:
				adj.append(new_pos)

		for ad in adj:
			if ad[0] == end[0] and ad[1] == end[1]:
				return curr_dist + 1
			else:
				if ad not in dists:
					to_check.append(ad)
					dists[ad] = curr_dist + 1
				elif curr_dist + 1 < dists[ad]:
					to_check.append(ad)
					dists[ad] = curr_dist + 1


def part2():
	target = (max_x, 0)

	start_location = (0, 0)
	start_disk = nodes[start_location]

	# find zero disk
	zero_location = None
	for node in nodes:
		if nodes[node][1] == 0:
			zero_location = node
			break

	# find large disks

	# make grid
	grid = [["." for x in range(0, max_x + 1)] for y in range(0, max_y + 1)]
	for y in range(0, max_y + 1):
		for x in range(0, max_x + 1):
			if x == 0 and y == 0:
				grid[y][x] = "S"
			elif x == target[0] and y == target[1]:
				grid[y][x] = "T"
			elif x == zero_location[0] and y == zero_location[1]:
				grid[y][x] = "E"
			else:
				data = nodes[(x, y)]
				if data[1] > start_disk[0]:
					grid[y][x] = "#"

	walls = ["#"]

	steps = 0

	# steps to first get in front of target
	curr_target_pos = target
	curr_empty_pos = zero_location

	while curr_target_pos != start_location:
		in_front = (curr_target_pos[0] - 1, curr_target_pos[1])

		curr_steps = bfs(curr_empty_pos, in_front, grid, walls, [curr_target_pos])
		curr_steps += 1
		steps += curr_steps

		curr_empty_pos = curr_target_pos
		curr_target_pos = in_front

	return steps


p1()
p2()
