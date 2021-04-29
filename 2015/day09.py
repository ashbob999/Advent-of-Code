from typing import Callable
from os.path import isfile, join as path_join

file_name = path_join('input', 'day09.txt')


def to_list(mf: Callable = int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]


def to_gen(mf: Callable = int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)


if not isfile(file_name):
	from aoc import get_input_file

	get_input_file()

locations = []
dists = {}
for line in open(file_name).read().strip().split("\n"):
	places, distance = line.split("=")
	distance = int(distance.strip())
	places = places.strip().split("to")

	p1 = places[0].strip()
	p2 = places[1].strip()

	if p1 in dists:
		dists[p1][p2] = distance
	else:
		dists[p1] = {p2: distance}

	if p2 in dists:
		dists[p2][p1] = distance
	else:
		dists[p2] = {p1: distance}

	locations.append((p1, p2, distance))


def get_dist(curr, visited: set, cmp_func, start_dist):
	total_dist = start_dist
	visited.add(curr)

	if len(visited) == len(dists):
		return 0

	for next in dists[curr]:
		if next not in visited:
			vc = visited.copy()
			dist = get_dist(next, vc, cmp_func, start_dist) + dists[curr][next]
			total_dist = cmp_func(total_dist, dist)

	return total_dist


def part1():
	dist = 1000000000
	for start in dists.keys():
		dist = min(dist, get_dist(start, set(), min, 10000000000))

	return dist


def part2():
	dist = 0
	for start in dists.keys():
		dist = max(dist, get_dist(start, set(), max, 0))

	return dist


print(part1())
print(part2())
