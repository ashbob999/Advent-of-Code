from typing import Callable
from os.path import isfile, join as path_join

file_name = path_join('input', 'day11.txt')


def to_list(mf: Callable = int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]


def to_gen(mf: Callable = int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)


if not isfile(file_name):
	from aoc import get_input_file

	get_input_file()

from intcode_machine import IntCodeVM

instr = list(map(int, open(file_name).read().strip().split(",")))


def pad_list(arr, amount):
	for i in range(amount):
		arr.append(0)


pad_list(instr, len(instr) * 2)


def get_visited(inp):
	vm = IntCodeVM(instr[:], [inp])

	robot_pos = [0, 0]
	visited = {}
	# black = 0
	# white = 1

	dirs = ["up", "right", "down", "left"]
	dir = "up"

	vm.run()
	while not vm.finished:
		outputs = vm.program_outputs[-2:]
		# if tuple(robot_pos) in visited:
		visited[tuple(robot_pos)] = outputs[0]

		if outputs[1] == 0:  # turn left
			dir_index = dirs.index(dir) - 1
			if dir_index < 0:
				dir_index = len(dirs) - 1
		else:  # turn right
			dir_index = dirs.index(dir) + 1
			if dir_index >= len(dirs):
				dir_index = 0

		dir = dirs[dir_index]

		if dir == "up":
			robot_pos = [robot_pos[0], robot_pos[1] + 1]
		elif dir == "right":
			robot_pos = [robot_pos[0] + 1, robot_pos[1]]
		elif dir == "down":
			robot_pos = [robot_pos[0], robot_pos[1] - 1]
		elif dir == "left":
			robot_pos = [robot_pos[0] - 1, robot_pos[1]]

		if tuple(robot_pos) in visited:
			colour = visited[tuple(robot_pos)]
		else:
			colour = 0

		vm.add_input(colour)

	return visited


def part1():
	return len(get_visited(0))


def part2():
	visited = get_visited(1)

	min_x = min(visited, key=lambda x: x[0])[0]
	min_y = min(visited, key=lambda x: x[1])[1]

	max_x = max(visited, key=lambda x: x[0])[0]
	max_y = max(visited, key=lambda x: x[1])[1]

	img_width = abs(max_x - min_x)
	img_height = abs(max_y - min_y)

	pixels_to_add = {}
	for k, v in visited.items():
		new_pos = [k[0] + abs(min_x), k[1] + abs(min_y)]
		pixels_to_add[tuple(new_pos)] = v

	pixels = [[0 for _ in range(img_width + 5)] for _ in range(img_height + 5)]

	for k, v in pixels_to_add.items():
		if v == 1:
			pixels[k[1]][k[0]] = 1

	for y in range(img_height, -1, -1):
		print("".join(map(str, pixels[y])).replace("0", " ").replace("1", "\u2588"))


print(part1())
part2()
