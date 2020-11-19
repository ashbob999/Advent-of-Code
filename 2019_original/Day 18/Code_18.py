from pathfinding.core.diagonal_movement import DiagonalMovement as DM
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder

with open("Data_18.txt", "r") as file:
	lines = [line.strip() for line in file]

# part 1

player_pos = None
keys = {}
doors = {}

for i, line in enumerate(lines):
	print(line)
	for j, c in enumerate(line):
		if c == "@":
			player_pos = (j, i)
		elif c.isalpha():
			if c.isupper():
				doors[c] = (j, i)
			else:
				keys[c] = (j, i)

print()

grid_ = [[0 for x_ in range(81)] for y_ in range(81)]

for i_, l_ in enumerate(lines):
	for j_, c_ in enumerate(l_):
		if c_ != "#":
			grid_[i_][j_] = 1


def get_path(start_, end_, grid_param):
	grid_path = Grid(matrix=grid_param)
	start_node = grid_path.node(*start_)
	end_node = grid_path.node(*end_)

	# finder = BreadthFirstFinder(diagonal_movement=DM.never)
	finder = AStarFinder(diagonal_movement=DM.never)
	path, runs = finder.find_path(start_node, end_node, grid_path)

	return path


nodes = ["@", *doors.keys(), *keys.keys()]
node_pos = dict()
node_pos.update({"@": player_pos})
node_pos.update(doors)
node_pos.update(keys)


def do_bfs(start, to_find):
	# print(to_find)
	toExplore = []
	node_dist_ = dict()
	dy = [-1, 0, 1, 0]
	dx = [0, 1, 0, -1]

	visited = [[False for x in range(len(lines[y]))] for y in range(len(lines))]

	toExplore.append((start, 0))
	visited[start[1]][start[0]] = True

	while (len(toExplore) != 0):
		curPos, curDis = toExplore.pop(0)
		curX, curY = curPos
		gridChar = lines[curY][curX]
		if (gridChar in to_find and lines[start[1]][start[0]] != gridChar):
			node_dist_[gridChar] = curDis
		# print(gridChar)
		else:
			for i in range(4):
				newX = curX + dx[i]
				newY = curY + dy[i]
				if (lines[newY][newX] != "#"):
					if (not visited[newY][newX]):
						visited[newY][newX] = True
						toExplore.append(((newX, newY), curDis + 1))
	# print(node_dist_)
	return node_dist_


node_dist = dict()

for node in nodes:
	node_dist[node] = dict()

for curr_node in nodes:
	node_dist[curr_node] = do_bfs(node_pos[curr_node], nodes)

for n in node_dist.keys():
	break
	print(node, node_dist[n])

# 5000 - 6488: 6162

path = "fziblrsodauepckjmtxvhgnyw"

total_steps = 0

total_steps += len(get_path(player_pos, keys[path[0]], grid_)) - 1

for i in range(1, len(path)):
	start = keys[path[i - 1]]
	end = keys[path[i]]
# total_steps += len(get_path(start, end, grid_)) -1

print("Part 1: ", total_steps)

# part 2

"""
@ -> w
@ -> y
@ -> a -> p
@ -> e -> q
"""

total_steps = 0

# @ -> w
total_steps += len(get_path(player_pos, keys["w"], grid_)) - 1
total_steps += len(get_path(keys["w"], keys["v"], grid_)) - 1

# @ -> y
total_steps += len(get_path(player_pos, keys["h"], grid_)) - 1
# total_steps += len(get_path(keys["y"], keys["h"], grid_)) -1

# @ -> a -> p
total_steps += len(get_path(player_pos, keys["p"], grid_)) - 1
total_steps += len(get_path(keys["p"], keys["a"], grid_)) - 1
# total_steps += len(get_path(keys["a"], keys["u"], grid_)) -1

# @ -> e -> q
total_steps += len(get_path(player_pos, keys["e"], grid_)) - 1 - 2
total_steps += len(get_path(keys["e"], keys["q"], grid_)) - 1

print("Part 2: ", total_steps)
# 1240 - 2000: 1556
