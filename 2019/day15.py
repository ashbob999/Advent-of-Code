from typing import Callable
from os.path import isfile, join as path_join
file_name = path_join('input', 'day15.txt')
def to_list(mf: Callable = int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]
def to_gen(mf: Callable = int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)

if not isfile(file_name):
	from aoc import get_input_file
	get_input_file()

from intcode_machine import IntCodeVM

instr = list(map(int, open(file_name).read().strip().split(",")))

def get_4_dirs(current, grid):
	dirs = []
	dirs.append((current[0], current[1] - 1))  # north
	dirs.append((current[0], current[1] + 1))  # south
	dirs.append((current[0] - 1, current[1]))  # west
	dirs.append((current[0] + 1, current[1]))  # east

	return {i + 1: dir if grid.get(dir, None) != 0 else None for i, dir in enumerate(dirs)}


def part1():
	vm = IntCodeVM(instr, [])

	start = (0, 0)
	
	# 1: north
	# 2: south
	# 3: west
	# 4: east

	# 0: wall
	# 1: empty
	# 2: goal
	grid = {}
	grid[start] = 1
	
	goal_found = False

	current_pos = start

	dir_to_go = 0
	previous_dirs = []

	while not goal_found:
		dirs = get_4_dirs(current_pos, grid)

		unvisited_dirs = []
		for k, v in dirs.items():
			if v is not None:
				if v not in grid:
					unvisited_dirs.append(k)

		backtrack = False

		if len(unvisited_dirs) > 0:
			dir_to_go = unvisited_dirs[0]
		else:
			backtrack = True
			old_dir = previous_dirs[-1]
			previous_dirs.pop()

			if old_dir == 1:
				dir_to_go = 2
			elif old_dir == 2:
				dir_to_go = 1
			elif old_dir == 3:
				dir_to_go = 4
			elif old_dir == 4:
				dir_to_go = 3

		vm.add_input(dir_to_go)

		code = vm.program_outputs[-1]

		if code == 0:
			blocked_pos = dirs[dir_to_go]
			grid[blocked_pos] = 0
		else:
			current_pos = dirs[dir_to_go]

			if not backtrack:
				previous_dirs.append(dir_to_go)

			if code == 1:
				grid[current_pos] = 1
			elif code == 2:
				grid[current_pos] = 2
				goal_found = True

	return grid, len(previous_dirs)

def part2(grid):
	path_count = 0
	oxygen_pos = None
	path_pos = []

	for k, v in grid.items():
		if v == 1 or v == 2:
			path_count += 1
			path_pos.append(k)
		if v == 2:
			oxygen_pos = k

	to_check = {}
	checked = {}

	to_check[oxygen_pos] = 0

	while len(to_check) > 0:
		c_pos = list(to_check.keys())[0]
		prev_dist = to_check[c_pos]

		to_check.pop(c_pos, None)
		checked[c_pos] = prev_dist

		adj_pos = []
		adj_pos.append((c_pos[0], c_pos[1] - 1))  # north
		adj_pos.append((c_pos[0], c_pos[1] + 1))  # south
		adj_pos.append((c_pos[0] - 1, c_pos[1]))  # west
		adj_pos.append((c_pos[0] + 1, c_pos[1]))  # east

		for p in adj_pos:
			if p in path_pos:
				if p not in checked:
					to_check[p] = prev_dist + 1

	# time.sleep(1)

	max_dist = max(list(checked.values()))
	
	return max_dist


grid, p1 = part1()
print(p1)
print(part2(grid))
