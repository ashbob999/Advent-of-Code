from intcode import IntCodeVM

with open("Data_15.txt", "r") as file:
	lines = [line.strip() for line in file]

instr = list(map(int, lines[0].split(",")))

# part 1

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


def get_4_dirs(current):
	dirs = []
	dirs.append((current[0], current[1] - 1))  # north
	dirs.append((current[0], current[1] + 1))  # south
	dirs.append((current[0] - 1, current[1]))  # west
	dirs.append((current[0] + 1, current[1]))  # east

	return {i + 1: dir if grid.get(dir, None) != 0 else None for i, dir in enumerate(dirs)}


goal_found = False

current_pos = start

dir_to_go = 0
previous_dirs = []

while not goal_found:
	dirs = get_4_dirs(current_pos)

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

print("ended")

min_x = min(list(grid.keys()), key=lambda x: x[0])[0]
min_y = min(list(grid.keys()), key=lambda x: x[1])[1]

max_x = max(list(grid.keys()), key=lambda x: x[0])[0]
max_y = max(list(grid.keys()), key=lambda x: x[1])[1]

img_width = abs(max_x - min_x) + 1
img_height = abs(max_y - min_y) + 1

print("width: ", img_width, "  height: ", img_height)

# img = Image.new("RGB", (img_width +5, img_height +5))

grid_map = [["#"] * img_width for i in range(img_height)]
print("w ", len(grid_map[0]), "  h ", len(grid_map))

pixels_to_add = {}
for k, v in grid.items():
	new_pos = [k[0] + abs(min_x), k[1] + abs(min_y)]
	pixels_to_add[tuple(new_pos)] = v

	type = "#"
	if k == (0, 0):
		type = "X"
	elif v == 2:
		type = "O"
	elif v == 1:
		type = " "
	# print(new_pos)
	grid_map[new_pos[0]][new_pos[1]] = type

for r in grid_map:
	print("".join(r))

print("Part 1: ", len(previous_dirs))

# part 2

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

print("Part 2: ", max_dist)
