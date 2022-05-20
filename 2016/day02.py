# @formatter:off
from os.path import isfile, join as path_join
from sys import path as sys_path
sys_path.insert(1, path_join(sys_path[0], '..'))
file_name = path_join('input', 'day02.txt')
def to_list(mf: object = int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]
def to_gen(mf: object = int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)
def p1(*args): ans = part1(*args); print(ans); return ans
def p2(*args): ans = part2(*args); print(ans); return ans

if not isfile(file_name):
	from aoc import get_input_file
	get_input_file()
# @formatter:on

from utils import parsefile

buttons = parsefile(file_name, [[str, ""], "\n"])


def part1():
	code = ""

	button_locations = {(-1, -1): "1", (0, -1): "2", (1, -1): "3", (-1, 0): "4", (0, 0): "5", (1, 0): "6", (-1, 1): "7",
	                    (0, 1): "8", (1, 1): "9"}

	button_locations_keys = set(button_locations)

	x = 0
	y = 0

	for button in buttons:
		for move in button:
			if move == "U":
				if (x, y - 1) in button_locations_keys:
					y -= 1
			elif move == "D":
				if (x, y + 1) in button_locations_keys:
					y += 1
			elif move == "L":
				if (x - 1, y) in button_locations_keys:
					x -= 1
			elif move == "R":
				if (x + 1, y) in button_locations_keys:
					x += 1

		code += button_locations[(x, y)]

	return code


def part2():
	code = ""

	button_locations = {(0, -2): "1", (-1, -1): "2", (0, -1): "3", (1, -1): "4", (-2, 0): "5", (-1, 0): "6",
	                    (0, 0): "7", (1, 0): "8", (2, 0): "9", (-1, 1): "A", (0, 1): "B", (1, 1): "C", (0, 2): "D"}

	button_locations_keys = set(button_locations)

	x = 0
	y = 0

	for button in buttons:
		for move in button:
			if move == "U":
				if (x, y - 1) in button_locations_keys:
					y -= 1
			elif move == "D":
				if (x, y + 1) in button_locations_keys:
					y += 1
			elif move == "L":
				if (x - 1, y) in button_locations_keys:
					x -= 1
			elif move == "R":
				if (x + 1, y) in button_locations_keys:
					x += 1

		code += button_locations[(x, y)]

	return code


p1()
p2()
