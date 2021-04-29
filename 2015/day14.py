from typing import Callable
from os.path import isfile, join as path_join

file_name = path_join('input', 'day14.txt')


def to_list(mf: Callable = int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]


def to_gen(mf: Callable = int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)


if not isfile(file_name):
	from aoc import get_input_file

	get_input_file()

reindeers = {}
seconds = 2503

for line in open(file_name).read().strip().split("\n"):
	parts = line.split()

	name: str = parts[0]
	speed: int = int(parts[3])
	time: int = int(parts[6])
	rest: int = int(parts[13])
	interval: int = time + rest
	dist_per_interval: int = speed * time

	reindeers[name] = (speed, time, rest, interval, dist_per_interval)


def part1():
	max_dist = 0
	for name, stats in reindeers.items():
		full_cycles = seconds // stats[3]
		rem = stats[3] % seconds

		dist = full_cycles * stats[4]

		if stats[1] >= rem:  # still flying
			dist += rem * stats[0]
		else:  # resting
			dist += stats[4]

		max_dist = max(max_dist, dist)

	return max_dist


def part2():
	deers = {name: [0, 0, True, 0] for name, stats in reindeers.items()}  # name: [time, dist, isMoving, points]

	for i in range(seconds):
		for name in deers.keys():
			if deers[name][2]:  # moving
				deers[name][0] += 1
				deers[name][1] += reindeers[name][0]
				if deers[name][0] == reindeers[name][1]:
					deers[name][0] = 0
					deers[name][2] = False  # now resting
			else:  # resting
				deers[name][0] += 1
				if deers[name][0] == reindeers[name][2]:
					deers[name][0] = 0
					deers[name][2] = True  # now moving

		max_dist = max(map(lambda x: deers[x][1], deers.keys()))
		highest = filter(lambda x: deers[x][1] == max_dist, deers.keys())
		for deer in highest:
			deers[deer][3] += 1

	return max(map(lambda x: deers[x][3], deers.keys()))


print(part1())
print(part2())
