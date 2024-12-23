# @formatter:off
from os.path import isfile, join as path_join
from sys import path as sys_path
sys_path.insert(1, path_join(sys_path[0], '..'))
file_name = path_join('input', 'day20.txt')
def to_list(mf=int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]
def to_gen(mf=int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)
def p1(*args): ans = part1(*args); print(ans); return ans
def p2(*args): ans = part2(*args); print(ans); return ans

if not isfile(file_name):
	from aoc import get_input_file
	get_input_file(session_path=['..', '.env'])
# @formatter:on

from utils import *

grid = parsefile(file_name, [list, "\n"])

saved = 100

w = len(grid[0])
h = len(grid)

start = None
end = None

for y in range(h):
	for x in range(w):
		if grid[y][x] == "S":
			start = (x, y)
		elif grid[y][x] == "E":
			end = (x, y)

adj = ((0, 1), (0, -1), (1, 0), (-1, 0))


def calc_rev_scores(s, e, grid):
	scores = {e: 0}

	to_check = [e]

	while len(to_check):
		curr = to_check.pop(0)
		score = scores[curr]

		for dx, dy in adj:
			nx = curr[0] + dx
			ny = curr[1] + dy

			if nx >= 0 and nx < w and ny >= 0 and ny < h and grid[ny][nx] != "#":
				ns = score + 1
				if (nx, ny) not in scores:
					scores[(nx, ny)] = ns
					to_check.append((nx, ny))

	return scores


scores = calc_rev_scores(start, end, grid)


def get_cheat_saves(length):
	c = 0

	for y in range(h):
		for x in range(w):
			if grid[y][x] == "#":
				continue

			for y2 in range(h):
				if abs(y - y2) > length:
					continue
				if y2 > y and y2 - y > length:
					break

				for x2 in range(w):
					if grid[y2][x2] == "#":
						continue

					if abs(x - x2) > length:
						continue
					if x2 > x and x2 - x > length:
						break

					if (x, y) == (x2, y2):
						continue

					dist = abs(x - x2) + abs(y - y2)
					if dist <= length:
						s1 = scores[(x, y)]
						s2 = scores[(x2, y2)]

						if s2 < s1:
							diff = s1 - s2 - dist
							if diff >= saved:
								c += 1

	return c


def part1():
	return get_cheat_saves(2)


def part2():
	return get_cheat_saves(20)


p1()
p2()
