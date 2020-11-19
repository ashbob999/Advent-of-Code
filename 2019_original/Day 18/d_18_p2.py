#!/usr/bin/env python3

import heapq


# sys.path.append(str(pathlib.Path(__file__).resolve().parent.parent / 'lib'))

# import aoc


def parse_grid(lines):
	grid = {}
	doors = {}
	keys = {}

	pos = None

	for y, row in enumerate(lines):
		for x, cell in enumerate(row):
			grid[(x, y)] = cell

			if cell == "@":
				pos = (x, y)
			elif cell >= "a" and cell <= "z":
				keys[cell] = (x, y)
			elif cell >= "A" and cell <= "Z":
				doors[cell.lower()] = (x, y)

	return grid, doors, keys, pos


def render_grid(grid):
	min_x = min(x for x, _ in grid.keys())
	min_y = min(y for _, y in grid.keys())
	max_x = max(x for x, _ in grid.keys())
	max_y = max(y for _, y in grid.keys())

	grid_str = "\n".join(("".join(grid[(x, y)] for x in range(min_x, max_x + 1))) for y in range(min_y, max_y + 1))
	print(f"{grid_str}\n")


def update_grid(grid, pos):
	all_pos = []

	grid[pos] = "#"
	for dx, dy in ((0, -1), (1, 0), (0, 1), (-1, 0)):
		pt = (pos[0] + dx, pos[1] + dy)
		grid[pt] = "#"

	for dx, dy in ((1, -1), (1, 1), (-1, 1), (-1, -1)):
		pt = (pos[0] + dx, pos[1] + dy)
		all_pos.append(pt)
		grid[pt] = "@"

	return all_pos


def shortest_path(grid, p1, p2):
	path_steps = None
	doors = set()
	visited = set()

	q = [(0, p1, set())]

	while len(q):
		steps, pos, doors = heapq.heappop(q)
		visited.add(pos)

		if pos == p2:
			path_steps = steps
			break

		if grid[pos] >= "A" and grid[pos] <= "Z":
			doors = doors.copy()
			doors.add(grid[pos].lower())

		for dx, dy in ((0, -1), (1, 0), (0, 1), (-1, 0)):
			nx, ny = pos[0] + dx, pos[1] + dy
			if grid.get((nx, ny), "#") != "#" and (nx, ny) not in visited:
				heapq.heappush(q, (steps + 1, (nx, ny), doors))

	return path_steps, doors


def find_key_paths(grid, doors, keys, starts):
	keypaths = {k: {} for k in keys.keys()}

	for i, pos in enumerate(starts):
		keypaths["@" + str(i)] = {}

		for key, key_pt in keys.items():
			steps, doors = shortest_path(grid, starts[i], key_pt)
			if steps is not None:
				keypaths["@" + str(i)][key] = {"pos": key_pt, "steps": steps, "doors": doors}

			for dest, dest_pt in keys.items():
				if dest != key and key not in keypaths[dest]:
					steps, doors = shortest_path(grid, key_pt, dest_pt)
					if steps is not None:
						keypaths[key][dest] = {"pos": dest_pt, "steps": steps, "doors": doors}
						keypaths[dest][key] = {"pos": key_pt, "steps": steps, "doors": doors}

	return keypaths


def find_keys(grid, keypaths, pos, bot_id="@0", key="@0", found=None, cache={}):
	if found is None:
		found = set(x for x in keypaths.keys() if x[0] == "@")

	pos[bot_id] = key

	if len(found) == len(keypaths):
		return 0, [key]

	cachekey = "".join(sorted(pos.values())) + "".join(sorted(set(keypaths.keys()) - found))
	if cachekey not in cache:
		paths = []

		for bot, bot_key in pos.items():
			for k in keypaths[bot]:
				if k in found:
					continue
				elif keypaths[bot_key][k]["doors"] - found != set():
					continue

				ksteps, kpaths = find_keys(grid, keypaths, pos.copy(), bot, k, found | {k}, cache)
				paths.append((keypaths[bot_key][k]["steps"] + ksteps, [key] + kpaths))

		cache[cachekey] = min(paths)

	return cache[cachekey]


def run():
	# input_file = aoc.inputfile('input.txt')
	lines = open("Data_18.txt").read().strip()

	grid, doors, keys, pos = parse_grid(lines.split("\n"))
	render_grid(grid)

	keypaths = find_key_paths(grid, doors, keys, [pos])
	steps, keypath = find_keys(grid, keypaths, {"@0": "@0"})
	print(f"Steps to find all keys: {steps}\nPath: {keypath[1:]})")

	all_pos = update_grid(grid, pos)
	keypaths = find_key_paths(grid, doors, keys, all_pos)
	steps, keypath = find_keys(grid, keypaths, {"@" + str(i): "@" + str(i) for i in range(0, len(all_pos))})
	print(f"Steps to find all keys: {steps}\nPath: {keypath}")


run()
