# @formatter:off
from os.path import isfile, join as path_join
from sys import path as sys_path
sys_path.insert(1, path_join(sys_path[0], '..'))
file_name = path_join('input', 'day11.txt')
def to_list(mf: object = int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]
def to_gen(mf: object = int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)
def p1(*args): ans = part1(*args); print(ans); return ans
def p2(*args): ans = part2(*args); print(ans); return ans

if not isfile(file_name):
	from aoc import get_input_file
	get_input_file(session_path=['..', '.env'])
# @formatter:on

from utils import parsefile

moves = parsefile(file_name, [str, ","])


# pos = [0, 0]
# n = [0, -2]
# nw = [-1, -1]
# ne = [1, -1]
# s = [0, 2]
# sw = [-1, 1]
# se = [1, 1]


def part1():
	pos = [0, 0]

	for move in moves:
		if move == "n":
			pos = [pos[0], pos[1] - 2]
		elif move == "nw":
			pos = [pos[0] - 1, pos[1] - 1]
		elif move == "ne":
			pos = [pos[0] + 1, pos[1] - 1]
		elif move == "s":
			pos = [pos[0], pos[1] + 2]
		elif move == "sw":
			pos = [pos[0] - 1, pos[1] + 1]
		elif move == "se":
			pos = [pos[0] + 1, pos[1] + 1]

	dist = abs(pos[0]) + abs(pos[1])
	dist //= 2

	return dist


def part2():
	pos = [0, 0]
	furthest = 0

	for move in moves:
		if move == "n":
			pos = [pos[0], pos[1] - 2]
		elif move == "nw":
			pos = [pos[0] - 1, pos[1] - 1]
		elif move == "ne":
			pos = [pos[0] + 1, pos[1] - 1]
		elif move == "s":
			pos = [pos[0], pos[1] + 2]
		elif move == "sw":
			pos = [pos[0] - 1, pos[1] + 1]
		elif move == "se":
			pos = [pos[0] + 1, pos[1] + 1]

		dist = abs(pos[0]) + abs(pos[1])
		if dist > furthest:
			furthest = dist

	furthest //= 2

	return furthest


p1()
p2()
