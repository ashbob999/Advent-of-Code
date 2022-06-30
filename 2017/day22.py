# @formatter:off
from os.path import isfile, join as path_join
from sys import path as sys_path
sys_path.insert(1, path_join(sys_path[0], '..'))
file_name = path_join('input', 'day22.txt')
def to_list(mf: object = int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]
def to_gen(mf: object = int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)
def p1(*args): ans = part1(*args); print(ans); return ans
def p2(*args): ans = part2(*args); print(ans); return ans

if not isfile(file_name):
	from aoc import get_input_file
	get_input_file(session_path=['..', '.env'])
# @formatter:on

from utils import parsefile

grid = parsefile(file_name, [list, "\n"])

width = len(grid[0])
height = len(grid)

infected_points = set()
for y in range(height):
	for x in range(width):
		if grid[y][x] == "#":
			infected_points.add((x, y))


def part1():
	inf_points = infected_points.copy()
	pos = [width // 2, height // 2]
	inf_cnt = 0
	dir = 0  # up

	for i in range(10000):
		if (pos[0], pos[1]) in inf_points:  # turn right
			dir += 1
			if dir == 4:
				dir = 0

			# clean
			inf_points.remove((pos[0], pos[1]))
		else:  # turn left
			dir -= 1
			if dir == -1:
				dir = 3

			# infect
			inf_points.add((pos[0], pos[1]))
			inf_cnt += 1

		# move
		if dir == 0:  # up
			pos[1] -= 1
		elif dir == 2:  # down
			pos[1] += 1
		elif dir == 1:  # right
			pos[0] += 1
		elif dir == 3:  # left
			pos[0] -= 1

	return inf_cnt


def part2():
	inf_points = {p: 2 for p in infected_points}

	pos = [width // 2, height // 2]
	inf_cnt = 0
	dir = 0  # up

	for i in range(10000000):
		if (pos[0], pos[1]) not in inf_points:
			inf_points[(pos[0], pos[1])] = 0  # clean
		state = inf_points[(pos[0], pos[1])]
		if state == 0:  # clean, turn left
			dir -= 1
			if dir == -1:
				dir = 3

			# clean -> weakened
			inf_points[(pos[0], pos[1])] = 1
		elif state == 1:  # weakened, carry on
			# weakened -> infected
			inf_points[(pos[0], pos[1])] = 2

			inf_cnt += 1
		elif state == 2:  # infected, turn right
			dir += 1
			if dir == 4:
				dir = 0

			# infected -> flagged
			inf_points[(pos[0], pos[1])] = 3
		elif state == 3:  # flagged, reverse dir
			dir -= 2
			if dir < 0:
				dir += 4

			# flagged -> clean
			inf_points[(pos[0], pos[1])] = 0

		# move
		if dir == 0:  # up
			pos[1] -= 1
		elif dir == 2:  # down
			pos[1] += 1
		elif dir == 1:  # right
			pos[0] += 1
		elif dir == 3:  # left
			pos[0] -= 1

	# print(inf_points, pos)

	return inf_cnt


p1()
p2()
