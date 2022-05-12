# @formatter:off
from os.path import isfile, join as path_join
from sys import path as sys_path
sys_path.insert(1, path_join(sys_path[0], '..'))
file_name = path_join('input', 'day01.txt')
def to_list(mf: object = int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]
def to_gen(mf: object = int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)
def p1(*args): ans = part1(*args); print(ans); return ans
def p2(*args): ans = part2(*args); print(ans); return ans

if not isfile(file_name):
	from aoc import get_input_file
	get_input_file()
# @formatter:on

from utils import parsefile, Merge

dirs = parsefile(file_name, [[str, Merge(int), 0, ""], ", "])


def part1():
	pos = [0, 0]
	facing = 0

	for dir in dirs:
		if dir[0] == "L":  # left
			facing -= 1
		else:  # right
			facing += 1

		facing %= 4

		if facing % 2 == 0:  # vertical
			index = 0
		else:  # horizontal
			index = 1

		if facing <= 1:  # positive
			sign = 1
		else:  # negative
			sign = -1

		pos[index] += sign * dir[1]

	dist = abs(pos[0]) + abs(pos[1])
	return dist


def part2():
	pos = [0, 0]
	facing = 0
	visited = set()
	visited.add(tuple(pos))

	for dir in dirs:
		if dir[0] == "L":  # left
			facing -= 1
		else:  # right
			facing += 1

		facing %= 4

		if facing % 2 == 0:  # vertical
			index = 0
		else:  # horizontal
			index = 1

		if facing <= 1:  # positive
			sign = 1
		else:  # negative
			sign = -1

		found = False

		for _ in range(dir[1]):
			pos[index] += sign
			if tuple(pos) in visited:
				found = True
				break
			else:
				visited.add(tuple(pos))

		if found:
			break

	dist = abs(pos[0]) + abs(pos[1])
	return dist


p1()
p2()
