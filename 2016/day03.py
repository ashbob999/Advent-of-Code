# @formatter:off
from os.path import isfile, join as path_join
from sys import path as sys_path
sys_path.insert(1, path_join(sys_path[0], '..'))
file_name = path_join('input', 'day03.txt')
def to_list(mf: object = int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]
def to_gen(mf: object = int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)
def p1(*args): ans = part1(*args); print(ans); return ans
def p2(*args): ans = part2(*args); print(ans); return ans

if not isfile(file_name):
	from aoc import get_input_file
	get_input_file()
# @formatter:on

from utils import parsefile

points = parsefile(file_name, [[int], "\n"])


def check(sides):
	s = sorted(sides)
	return s[0] + s[1] > s[2]


def part1():
	count = 0

	for sides in points:
		if check(sides):
			count += 1

	return count


def part2():
	count = 0

	for i in range(0, len(points), 3):
		for j in range(3):
			if check([points[i][j], points[i + 1][j], points[i + 2][j]]):
				count += 1

	return count


p1()
p2()
