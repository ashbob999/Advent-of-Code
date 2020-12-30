from os.path import isfile, join as path_join
from typing import Callable

file_name = path_join('input', 'day24.txt')


def to_list(mf: Callable = int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]


def to_gen(mf: Callable = int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)


if not isfile(file_name):
	from aoc import get_input_file

	get_input_file(session_path=['..', '.env'])

data = to_list(mf=str)

tiles = {}

def part1():

	for t in data:
		start = [0, 0]

		i = 0
		while i < len(t):
			if t[i] == "e":
				start[0] += 2
				i += 1
			elif t[i] == "w":
				start[0] -= 2
				i+= 1
			elif t[i] == "s":
				start[1] += 1
				if t[i+1] == "e":
					start[0] += 1
				elif t[i+1] == "w":
					start[0] -= 1
				i += 2
			elif t[i] == "n":
				start[1] -= 1
				if t[i+1] == "e":
					start[0] += 1
				elif t[i+1] == "w":
					start[0] -= 1
				i += 2

		if tuple(start) in tiles:
			tiles[tuple(start)] ^= 1
		else:
			tiles[tuple(start)] = 1

	count = 0
	for k, v in tiles.items():
		if v == 1:
			count += 1
		#print(k, v)

	print(count)

adj = ((-2, 0), (2, 0), (-1, -1), (1, -1), (-1, 1), (1, 1))


# print(len(set(adj)))

def part2():
	global tiles

	for i in range(100):
		new_tiles = tiles.copy()
		for tile, v in tiles.items():
			if v == 1:
				for ad in adj:
					at = [tile[0] + ad[0], tile[1] + ad[1]]
					if tuple(at) not in tiles:
						new_tiles[tuple(at)] = 0

		new_tiles2 = new_tiles.copy()

		for tile, v in new_tiles.items():
			bc = 0
			for ad in adj:
				at = [tile[0] + ad[0], tile[1] + ad[1]]
				if tuple(at) in tiles and new_tiles[tuple(at)] == 1:
					bc += 1

			if v == 1 and (bc == 0 or bc > 2):
				new_tiles2[tile] = 0

			if v == 0 and bc == 2:
				new_tiles2[tile] = 1

		tiles = new_tiles2

	# cc = 0
	# for k, v in tiles.items():
	# 	if v == 1:
	# 		cc += 1
	# print(i+1, cc)

	count = 0
	for t, v in tiles.items():
		if v == 1:
			count += 1

	print(count)

part1()
part2()
