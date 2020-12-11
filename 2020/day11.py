from os.path import isfile, join as path_join
from typing import Callable

file_name = path_join('input', 'day11.txt')


def to_list(mf: Callable = int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]


def to_gen(mf: Callable = int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)


if not isfile(file_name):
	from aoc import get_input_file

	get_input_file(session_path=['..', '.env'])

data = to_list(mf=list)

h = len(data)
w = len(data[0])

def part1():

	floor = [v[:] for v in data]

	while True:
		changed = 0

		nf = [r[:] for r in floor]

		for y in range(h):
			for x in range(w):
				adj = 0
				if y > 0 and floor[y - 1][x] == "#":
					adj += 1
				if y < h - 1 and floor[y + 1][x] == "#":
					adj += 1
				if x > 0 and floor[y][x - 1] == "#":
					adj += 1
				if x < w-1 and floor[y][x+1] == "#":
					adj += 1
				if y > 0 and x > 0 and floor[y-1][x-1] == "#":
					adj += 1
				if y > 0 and x < w-1 and floor[y-1][x+1] == "#":
					adj += 1
				if y < h-1 and x > 0 and floor[y+1][x-1] == "#":
					adj += 1
				if y < h-1 and x < w-1 and floor[y+1][x+1] == "#":
					adj += 1

				if floor[y][x] == "L" and adj == 0:
					nf[y][x] = "#"
					changed += 1

				elif floor[y][x] == "#" and adj >= 4:
					nf[y][x] = "L"
					changed += 1

		floor = nf

		if changed == 0:
			break

	c = 0
	for y in range(h):
		for x in range(w):
			if floor[y][x] == "#":
				c += 1

	print(c)


def dir(f, x, y, dy, dx):
	x += dx
	y += dy

	while x >= 0 and y >= 0 and x < w and y < h:
		if f[y][x] == "L":
			return False

		if f[y][x] == "#":
			return True

		x += dx
		y += dy

	return False


dirs = ((-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1))


def part2():
	floor = [v[:] for v in data]

	while True:
		changed = 0

		nf = [f[:] for f in floor]

		for y in range(h):
			for x in range(w):
				adj = 0

				for dir in dirs:
					tmp_x = x + dir[1]
					tmp_y = y + dir[0]

					while tmp_x >= 0 and tmp_y >= 0 and tmp_x < w and tmp_y < h:
						if floor[tmp_y][tmp_x] == "L":
							break

						if floor[tmp_y][tmp_x] == "#":
							adj += 1
							break

						tmp_x += dir[1]
						tmp_y += dir[0]

				# print(x,y,adj)

				if floor[y][x] == "L" and adj == 0:
					nf[y][x] = "#"
					changed += 1
				# print(y,x, floor[y][x], nf[y][x])

				elif floor[y][x] == "#" and adj >= 5:
					nf[y][x] = "L"
					changed += 1

		floor = nf  # [v[:] for v in nf]

		# for l in floor:
		# 	print("".join(l))

		# print(changed)
		# break
		if changed == 0:
			break

	c = 0
	for y in range(h):
		for x in range(w):
			if floor[y][x] == "#":
				c += 1

	print(c)


part1()
part2()
