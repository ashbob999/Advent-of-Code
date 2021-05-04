from typing import Callable
from os.path import isfile, join as path_join

file_name = path_join('input', 'day13.txt')


def to_list(mf: Callable = int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]


def to_gen(mf: Callable = int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)


if not isfile(file_name):
	from aoc import get_input_file

	get_input_file()

from intcode_machine import IntCodeVM

instr = list(map(int, open(file_name).read().strip().split(",")))


def chunks(l, n):
	n = max(1, n)
	return [l[i:i + n] for i in range(0, len(l), n)]


def pad_list(arr, amount):
	for i in range(amount):
		arr.append(0)


pad_list(instr, len(instr))


def part1():
	vm = IntCodeVM(instr, [])

	vm.run()

	output = vm.program_outputs

	tile_data = chunks(output, 3)

	tiles = {(t[0], t[1]): t[2] for t in tile_data}

	# 0: empty
	# 1: wall
	# 2: block
	# 3: horizontal paddle
	# 4: ball

	block_tile_count = 0

	for tile, type in tiles.items():
		if type == 2:
			block_tile_count += 1

	return block_tile_count


def part2():
	instr[0] = 2

	vm = IntCodeVM(instr, [0])
	vm.run()

	while not vm.finished:
		tile_data = chunks(vm.program_outputs, 3)

		tiles = {(t[0], t[1]): t[2] for t in tile_data}

		ball_pos = None
		paddle_pos = None
		block_count = 0

		for pos, type in tiles.items():
			if type == 3:
				paddle_pos = pos

			if type == 4:
				ball_pos = pos

			if type == 2:
				block_count += 1

		# print("ball: ", ball_pos, "  paddle: ", paddle_pos)
		# print("block count: ", block_count)

		if block_count == 0:
			vm.finished = True
			print("no blocks left")
			break

		joystick_move = 0

		if ball_pos[0] < paddle_pos[0]:
			joystick_move = -1
		else:
			joystick_move = 1

		vm.add_input(joystick_move)

	tile_data = chunks(vm.program_outputs, 3)

	tiles = {(t[0], t[1]): t[2] for t in tile_data}

	score = 0

	for pos, type in tiles.items():
		if pos == (-1, 0):
			score = type

	return score


print(part1())
print(part2())
