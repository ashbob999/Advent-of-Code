from typing import Callable
from os.path import isfile, join as path_join
file_name = path_join('input', 'day12.txt')
def to_list(mf: Callable = int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]
def to_gen(mf: Callable = int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)

if not isfile(file_name):
	from aoc import get_input_file
	get_input_file(session_path=['..', '.env'])


data = to_list(mf=str)

def part1():
	start = [0, 0]

	dir = 90

	for v in data:
		mov = v[0]
		amt = int(v[1:])

		if mov == "L":
			dir -= amt
			dir %= 360

		elif mov == "R":
			dir += amt
			dir %= 360

		elif mov == "N":
			start[1] += amt

		elif mov == "E":
			start[0] += amt

		elif mov == "S":
			start[1] -= amt

		elif mov == "W":
			start[0] -= amt

		elif mov == "F":
			if dir == 0:
				start[1] += amt
			elif dir == 90:
				start[0] += amt
			elif dir == 180:
				start[1] -= amt
			elif dir == 270:
				start[0] -= amt

	print(abs(start[0]) + abs(start[1]))


def part2():
	start = [0, 0]
	way = [10, -1]

	dir = 0

	for v in data:
		mov = v[0]
		amt = int(v[1:])

		if mov == "L":
			way = [[way[0], way[1]],
					[-way[1], way[0]],
					[-way[0], -way[1]],
					[way[1], -way[0]]][-amt // 90]

		elif mov == "R":
			way = [[way[0], way[1]],
					[-way[1], way[0]],
					[-way[0], -way[1]],
					[way[1], -way[0]]][amt // 90]

		elif mov == "N":
			way[1] -= amt

		elif mov == "E":
			way[0] += amt

		elif mov == "S":
			way[1] += amt

		elif mov == "W":
			way[0] -= amt

		elif mov == "F":
			start[0] += way[0] * amt
			start[1] += way[1] * amt


	print(abs(start[0]) + abs(start[1]))


part1()
part2()
