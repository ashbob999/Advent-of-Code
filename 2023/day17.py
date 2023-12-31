# @formatter:off
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
# @formatter:on

from utils import *

data = parsefile(file_name, [[int, ""], "\n"])

height = len(data)
width = len(data[0])

# dirs
# 0 up
# 1 right
# 2 down
# 3 left

dirs_go_left = {0: 3, 1: 0, 2: 1, 3: 2}
dirs_go_right = {0: 1, 1: 2, 2: 3, 3: 0}

dirs_move = {0: (0, -1), 1: (1, 0), 2: (0, 1), 3: (-1, 0)}


def move_pos(pos, dir):
	diff = dirs_move[dir]
	return pos[0] + diff[0], pos[1] + diff[1]


def get_next_pos(pos, dir, steps):
	# can only
	#   turn left
	#   turn right
	#   go straight

	next_pos = []

	# turn left
	left_dir = dirs_go_left[dir]
	next_pos.append((move_pos(pos, left_dir), left_dir, 1))

	# turn right
	right_dir = dirs_go_right[dir]
	next_pos.append((move_pos(pos, right_dir), right_dir, 1))

	# go straight
	next_pos.append((move_pos(pos, dir), dir, steps + 1))

	return next_pos


import heapq


def search(grid, start, end, min_steps, max_steps):
	if start == end:
		return []

	# (cost, pos, dir, steps_in_dir)
	to_check = []
	heapq.heappush(to_check, (0, start, 1, 0))
	heapq.heappush(to_check, (0, start, 2, 0))

	# (pos, dir, steps_in_dir)
	seen = set()

	while len(to_check) > 0:
		cost, curr, dir, steps = heapq.heappop(to_check)

		if curr == end and steps >= min_steps:
			return cost

		if (curr, dir, steps) in seen:
			continue

		seen.add((curr, dir, steps))

		for (next_pos, next_dir, next_steps) in get_next_pos(curr, dir, steps):
			if 0 <= next_pos[0] < width and 0 <= next_pos[1] < height:
				if (dir == next_dir and next_steps <= max_steps) or (dir != next_dir and steps >= min_steps):
					next_cost = cost + grid[next_pos[1]][next_pos[0]]
					heapq.heappush(to_check, (next_cost, next_pos, next_dir, next_steps))

	return None


def part1():
	cost = search(data, (0, 0), (width - 1, height - 1), 0, 3)
	return cost


def part2():
	cost = search(data, (0, 0), (width - 1, height - 1), 4, 10)
	return cost


p1()
p2()
