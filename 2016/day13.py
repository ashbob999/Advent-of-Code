# @formatter:off
from os.path import isfile, join as path_join
from sys import path as sys_path
sys_path.insert(1, path_join(sys_path[0], '..'))
file_name = path_join('input', 'day13.txt')
def to_list(mf: object = int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]
def to_gen(mf: object = int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)
def p1(*args): ans = part1(*args); print(ans); return ans
def p2(*args): ans = part2(*args); print(ans); return ans

if not isfile(file_name):
	from aoc import get_input_file
	get_input_file()
# @formatter:on

from utils import parsefile

number = int(parsefile(file_name, None))

target = (31, 39)

start = (1, 1)


def check(x, y):
	if x < 0 or y < 0:
		return 1  # wall
	v = x * x + 3 * x + 2 * x * y + y + y * y
	v += number

	# if v.bit_count() % 2 == 0: # python 3.10+
	if bin(v).count("1") % 2 == 0:
		return 0  # open space
	else:
		return 1  # wall


def search(start, end):
	left = [start]
	dist = {start: 0}

	while len(left) > 0:
		curr_pos = left.pop(0)
		curr_dist = dist[curr_pos]

		# get adjacent (h + v)
		adj = []
		for x in range(-1, 2, 2):
			new_pos = (curr_pos[0] + x, curr_pos[1])
			if check(new_pos[0], new_pos[1]) == 0:
				adj.append(new_pos)
		for y in range(-1, 2, 2):
			new_pos = (curr_pos[0], curr_pos[1] + y)
			if check(new_pos[0], new_pos[1]) == 0:
				adj.append(new_pos)

		# check dists
		for ad in adj:
			if ad[0] == target[0] and ad[1] == target[1]:
				return curr_dist + 1  # bfs
			else:
				if ad not in dist:
					dist[ad] = curr_dist + 1
					left.append(ad)
				elif curr_dist + 1 < dist[ad]:
					dist[ad] = curr_dist + 1
					left.append(ad)


def part1():
	steps = search(start, target)
	return steps


def bfs(start, limit):
	left = [start]
	dist = {start: 0}

	while len(left) > 0:
		curr_pos = left.pop(0)
		curr_dist = dist[curr_pos]

		# get adjacent (h + v)
		adj = []
		for x in range(-1, 2, 2):
			new_pos = (curr_pos[0] + x, curr_pos[1])
			if check(new_pos[0], new_pos[1]) == 0:
				adj.append(new_pos)
		for y in range(-1, 2, 2):
			new_pos = (curr_pos[0], curr_pos[1] + y)
			if check(new_pos[0], new_pos[1]) == 0:
				adj.append(new_pos)

		# check dists
		for ad in adj:
			if curr_dist + 1 <= limit:
				if ad not in dist:
					dist[ad] = curr_dist + 1
					left.append(ad)
				elif curr_dist + 1 < dist[ad]:
					dist[ad] = curr_dist + 1
					left.append(ad)

	return len(dist)


def part2():
	locations = bfs(start, 50)
	return locations


p1()
p2()
