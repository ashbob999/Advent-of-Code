from typing import Callable
from os.path import isfile, join as path_join
file_name = path_join('input', 'day11.txt')
def to_list(mf: Callable = int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]
def to_gen(mf: Callable = int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)

if not isfile(file_name):
	from aoc import get_input_file
	get_input_file(session_path=['..', '.env'])


data = to_list(mf=str)

adata = """L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL""".split("\n")

data = [list(s) for s in data]

#floor = [v[:] for v in data]

h = len(data)
w = len(data[0])

def part1():

	floor = [v[:] for v in data]


	while True:
		changed = 0

		nf = [f[:] for f in floor]

		for y in range(h):
			for x in range(w):
				adj = 0
				if y > 0 and floor[y-1][x] == "#":
					adj += 1
				if y < h-1 and floor[y+1][x] == "#":
					adj += 1
				if x > 0 and floor[y][x-1] == "#":
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

				#print(x,y,adj)

				if floor[y][x] == "L" and adj == 0:
					nf[y][x] = "#"
					changed += 1
					#print(y,x, floor[y][x], nf[y][x])

				elif floor[y][x] == "#" and adj >= 4:
					nf[y][x] = "L"
					changed += 1

		floor = [v[:] for v in nf]

		for l in floor:
			pass #print("".join(l))

		print(changed)
		#break
		if changed == 0:
			break

	c = 0
	for y in range(h):
		for x in range(w):
			if floor[y][x] == "#":
				c += 1

	print("part 1", c)

def dir(f, w, h, x, y, dy, dx):
	x += dx
	y += dy

	while x>=0 and y>=0 and x<w and y<h:
		if f[y][x] == "L":
			return False

		if f[y][x] == "#":
			return True

		x += dx
		y += dy

	return False

def part2():

	floor = [v[:] for v in data]


	while True:
		changed = 0

		nf = [f[:] for f in floor]

		for y in range(h):
			for x in range(w):
				adj = 0
				if dir(floor, w, h, x, y, -1, 0):
					adj += 1
				if dir(floor, w, h, x, y, 1, 0):
					adj += 1
				if dir(floor, w, h, x, y, 0, -1):
					adj += 1
				if dir(floor, w, h, x, y, 0, 1):
					adj += 1
				if dir(floor, w, h, x, y, -1, -1):
					adj += 1
				if dir(floor, w, h, x, y, -1, 1):
					adj += 1
				if dir(floor, w, h, x, y, 1, -1):
					adj += 1
				if dir(floor, w, h, x, y, 1, 1):
					adj += 1

				#print(x,y,adj)

				if floor[y][x] == "L" and adj == 0:
					nf[y][x] = "#"
					changed += 1
					#print(y,x, floor[y][x], nf[y][x])

				elif floor[y][x] == "#" and adj >= 5:
					nf[y][x] = "L"
					changed += 1

		floor = [v[:] for v in nf]

		for l in floor:
			pass #print("".join(l))

		print(changed)
		#break
		if changed == 0:
			break

	c = 0
	for y in range(h):
		for x in range(w):
			if floor[y][x] == "#":
				c += 1

	print("part 2", c)


part1()
part2()
