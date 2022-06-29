# @formatter:off
from os.path import isfile, join as path_join
from sys import path as sys_path
sys_path.insert(1, path_join(sys_path[0], '..'))
file_name = path_join('input', 'day12.txt')
def to_list(mf: object = int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]
def to_gen(mf: object = int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)
def p1(*args): ans = part1(*args); print(ans); return ans
def p2(*args): ans = part2(*args); print(ans); return ans

if not isfile(file_name):
	from aoc import get_input_file
	get_input_file(session_path=['..', '.env'])
# @formatter:on

from utils import parsefile, Merge

raw_pipes = parsefile(file_name, [[int, 1, None, 1, Merge([int, ","]), 0], "\n"])

pipes = {}
for pipe in raw_pipes:
	pipes[pipe[0]] = pipe[1:]


def bfs_group(target):
	visited = set()

	visited.add(target)

	to_check = pipes[target][:]

	while len(to_check) > 0:
		curr_value = to_check[0]
		to_check.pop(0)

		visited.add(curr_value)

		for p in pipes[curr_value]:
			if p not in visited:
				to_check.append(p)

	return visited


def part1():
	group_0 = bfs_group(0)
	return len(group_0)


def part2():
	all_values = set(pipes.keys())

	group_count = 0

	while len(all_values) > 0:
		curr_value = list(all_values)[0]

		group_set = bfs_group(curr_value)

		group_count += 1

		all_values.difference_update(group_set)

	return group_count


p1()
p2()
