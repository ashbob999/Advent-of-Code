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

input_num = parsefile(file_name, int)[0]


def spiral(n):
	pos = [0, 0]
	i = 1
	l = 0

	while (True):
		l += 2
		i += 1
		pos[0] += 1

		# right
		for j in range(l - 1):
			pos[1] -= 1
			i += 1
			if i == n:
				return pos

		# top
		for j in range(l):
			pos[0] -= 1
			i += 1
			if i == n:
				return pos

		# left
		for j in range(l):
			pos[1] += 1
			i += 1
			if i == n:
				return pos

		# bottom
		for j in range(l):
			pos[0] += 1
			i += 1
			if i == n:
				return pos


def part1():
	pos = spiral(input_num)

	return abs(pos[0]) + abs(pos[1])


def spiral2(n):
	def sum_locs(locs, pos):
		val = 0
		for x in range(-1, 2):
			for y in range(-1, 2):
				if x == 0 and y == 0:
					continue

				t = (pos[0] + x, pos[1] + y)
				if t in locs:
					val += locs[t]

		locs[(pos[0], pos[1])] = val
		return val

	locs = {(0, 0): 1}
	pos = [0, 0]
	i = 1
	l = 0

	while (True):
		l += 2
		i += 1
		pos[0] += 1
		v = sum_locs(locs, pos)
		if v > n:
			return v

		# right
		for j in range(l - 1):
			pos[1] -= 1
			i += 1
			v = sum_locs(locs, pos)
			if v > n:
				return v

		# top
		for j in range(l):
			pos[0] -= 1
			i += 1
			v = sum_locs(locs, pos)
			if v > n:
				return v

		# left
		for j in range(l):
			pos[1] += 1
			i += 1
			v = sum_locs(locs, pos)
			if v > n:
				return v

		# bottom
		for j in range(l):
			pos[0] += 1
			i += 1
			v = sum_locs(locs, pos)
			if v > n:
				return v


def part2():
	return spiral2(input_num)


p1()
p2()
