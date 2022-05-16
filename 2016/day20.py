# @formatter:off
from os.path import isfile, join as path_join
from sys import path as sys_path
sys_path.insert(1, path_join(sys_path[0], '..'))
file_name = path_join('input', 'day20.txt')
def to_list(mf: object = int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]
def to_gen(mf: object = int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)
def p1(*args): ans = part1(*args); print(ans); return ans
def p2(*args): ans = part2(*args); print(ans); return ans

if not isfile(file_name):
	from aoc import get_input_file
	get_input_file()
# @formatter:on

from utils import parsefile

blocked_ips = parsefile(file_name, [[int, "-"], "\n"])

blocked_ips = sorted(blocked_ips)

ranges = [blocked_ips[0]]
for curr_range in blocked_ips:
	prev_range = ranges[-1]
	if curr_range[0] <= prev_range[1] + 1:
		new_range = [prev_range[0], max(prev_range[1], curr_range[1])]
		ranges[-1] = new_range
	else:
		ranges.append(curr_range)


def part1():
	lowest_free_ip = ranges[0][1] + 1
	return lowest_free_ip


def part2():
	count = 0

	for i in range(0, len(ranges) - 1):
		count += ranges[i + 1][0] - ranges[i][1] - 1

	# last one
	count += 4294967295 - ranges[-1][1]

	return count


p1()
p2()
