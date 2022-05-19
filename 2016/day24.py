# @formatter:off
from os.path import isfile, join as path_join
from sys import path as sys_path
sys_path.insert(1, path_join(sys_path[0], '..'))
file_name = path_join('input', 'day24.txt')
def to_list(mf: object = int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]
def to_gen(mf: object = int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)
def p1(*args): ans = part1(*args); print(ans); return ans
def p2(*args): ans = part2(*args); print(ans); return ans

if not isfile(file_name):
	from aoc import get_input_file
	get_input_file()
# @formatter:on

from utils import parsefile

grid = parsefile(file_name, [[""], "\n"])

width = len(grid[0])
height = len(grid)

number_locations = {}

for y in range(1, height - 1):
	for x in range(1, width - 1):
		c = grid[y][x]
		if "0" <= c <= "9":
			number_locations[int(c)] = (x, y)


def bfs(start, end):
	to_check = [start]

	distances = {start: 0}

	while len(to_check) > 0:
		curr_pos = to_check.pop(0)

		curr_dist = distances[curr_pos]

		adj = []
		for y in range(-1, 2, 2):
			new_pos = (curr_pos[0], curr_pos[1] + y)
			if 0 < new_pos[1] < height - 1 and grid[new_pos[1]][new_pos[0]] != "#":
				adj.append(new_pos)

		for x in range(-1, 2, 2):
			new_pos = (curr_pos[0] + x, curr_pos[1])
			if 0 < new_pos[0] < width - 1 and grid[new_pos[1]][new_pos[0]] != "#":
				adj.append(new_pos)

		for ad in adj:
			if ad[0] == end[0] and ad[1] == end[1]:
				return curr_dist + 1
			else:
				if ad not in distances:
					distances[ad] = curr_dist + 1
					to_check.append(ad)
				elif curr_dist + 1 < distances[ad]:
					distances[ad] = curr_dist + 1
					to_check.append(ad)


from itertools import permutations as perm, combinations as comb

# calculate all of the dists
dists = {}

targets = list(number_locations.keys())
targets.remove(0)

# get dist for all a->b locations
for p in comb(targets, 2):
	start = number_locations[p[0]]
	end = number_locations[p[1]]
	dist = bfs(start, end)
	dists[p] = dist
	dists[(p[1], p[0])] = dist

# add dists for all 0-> locations
for t in targets:
	start = number_locations[0]
	end = number_locations[t]
	dist = bfs(start, end)
	dists[(0, t)] = dist
	dists[(t, 0)] = dist


def part1():
	min_dist = 100000000000000000

	for p in perm(targets):
		curr_dist = dists[(0, p[0])]
		for i in range(len(p) - 1):
			curr_dist += dists[(p[i], p[i + 1])]

		if curr_dist < min_dist:
			min_dist = curr_dist

	return min_dist


def part2():
	min_dist = 100000000000000000

	for p in perm(targets):
		curr_dist = dists[(0, p[0])]
		for i in range(len(p) - 1):
			curr_dist += dists[(p[i], p[i + 1])]

		curr_dist += dists[(p[-1], 0)]

		if curr_dist < min_dist:
			min_dist = curr_dist

	return min_dist


p1()
p2()
