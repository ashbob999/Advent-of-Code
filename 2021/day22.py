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

from utils import parsefile, parse

data = parsefile(file_name, [[str, [str, ","], " "], "\n"])

cubes = []
for v in data:
	state = v[0]
	xv = v[1][0][2:].split("..")
	yv = v[1][1][2:].split("..")
	zv = v[1][2][2:].split("..")

	xv = (int(xv[0]), int(xv[1]))
	yv = (int(yv[0]), int(yv[1]))
	zv = (int(zv[0]), int(zv[1]))

	cubes.append((state, xv, yv, zv))


def part1():
	on_cubes = set()
	for cube in cubes:
		if -50 <= cube[1][0] <= 50 and -50 <= cube[1][1] <= 50:
			if -50 <= cube[2][0] <= 50 and -50 <= cube[2][1] <= 50:
				if -50 <= cube[3][0] <= 50 and -50 <= cube[3][1] <= 50:
					for x in range(cube[1][0], cube[1][1] + 1):
						for y in range(cube[2][0], cube[2][1] + 1):
							for z in range(cube[3][0], cube[3][1] + 1):
								if cube[0] == "on":
									on_cubes.add((x, y, z))
								else:
									on_cubes.discard((x, y, z))

	return len(on_cubes)


def get_overlap(cube1, cube2):
	c1 = max(cube1[0]) < min(cube2[0]) or max(cube2[0]) < min(cube1[0])
	c2 = max(cube1[1]) < min(cube2[1]) or max(cube2[1]) < min(cube1[1])
	c3 = max(cube1[2]) < min(cube2[2]) or max(cube2[2]) < min(cube1[2])

	if c1 or c2 or c3:
		return None

	x1 = max(min(cube1[0]), min(cube2[0]))
	x2 = min(max(cube1[0]), max(cube2[0]))
	y1 = max(min(cube1[1]), min(cube2[1]))
	y2 = min(max(cube1[1]), max(cube2[1]))
	z1 = max(min(cube1[2]), min(cube2[2]))
	z2 = min(max(cube1[2]), max(cube2[2]))

	return (x1, x2), (y1, y2), (z1, z2)


def calc_volume(x_range, y_range, z_range):
	x = abs(x_range[1] - x_range[0]) + 1
	y = abs(y_range[1] - y_range[0]) + 1
	z = abs(z_range[1] - z_range[0]) + 1

	return x * y * z


def split(cube1, cube2):
	overlap = get_overlap(cube1, cube2)
	if overlap is None:
		return [cube1]

	new_cubes = [(cube1[0], cube1[1], (cube1[2][0], overlap[2][0] - 1)),
	             (cube1[0], cube1[1], (overlap[2][1] + 1, cube1[2][1])),
	             ((cube1[0][0], overlap[0][0] - 1), cube1[1], overlap[2]),
	             ((overlap[0][1] + 1, cube1[0][1]), cube1[1], overlap[2]),
	             (overlap[0], (cube1[1][0], overlap[1][0] - 1), overlap[2]),
	             (overlap[0], (overlap[1][1] + 1, cube1[1][1]), overlap[2])]

	return [(x, y, z) for x, y, z in new_cubes if x[0] <= x[1] and y[0] <= y[1] and z[0] <= z[1]]


def part2():
	volumes = []

	for i, cube in enumerate(cubes):
		state = cube[0]

		new_volumes = []

		for c in volumes:
			separate = split(c, cube[1:])
			new_volumes += separate

		if state == "on":
			new_volumes.append(cube[1:])

		volumes = new_volumes

	volume = 0
	for v in volumes:
		volume += calc_volume(*v)
	return volume


p1()
p2()
