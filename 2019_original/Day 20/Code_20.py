from collections import deque

with open("Data_20.txt", "r") as file:
	lines = [line for line in file]

maze = [list(line) for line in lines]

# part 1

dy = [-1, 0, 1, 0]
dx = [0, 1, 0, -1]

start = None  # on top
end = None  # on right

a_list = []
z_list = []

for i in range(len(maze)):
	for j in range(len(maze[i])):
		if maze[i][j] == "A":
			a_list.append((j, i))
		elif maze[i][j] == "Z":
			z_list.append((j, i))


def get_portal_name(x, y, grid):
	if grid[y - 1][x].isalpha():
		p_1 = grid[y - 1][x]
		p_2 = grid[y][x]
	elif grid[y + 1][x].isalpha():
		p_1 = grid[y][x]
		p_2 = grid[y + 1][x]
	elif grid[y][x - 1].isalpha():
		p_1 = grid[y][x - 1]
		p_2 = grid[y][x]
	elif grid[y][x + 1].isalpha():
		p_1 = grid[y][x]
		p_2 = grid[y][x + 1]

	return p_1 + p_2


def bfs(start_pos, grid, start_dist=0):
	to_visit = deque()
	visited = {}

	ends = {}

	visited[start_pos] = start_dist
	to_visit.append(start_pos)

	while len(to_visit) > 0:
		curr_pos = to_visit.popleft()
		curr_dist = visited[curr_pos]

		for i in range(4):
			next_x = curr_pos[0] + dx[i]
			next_y = curr_pos[1] + dy[i]
			next_pos = (next_x, next_y)

			if grid[next_y][next_x] != "#":
				if next_pos in visited:
					if curr_dist + 1 < visited[next_pos]:
						visited[next_pos] = curr_dist + 1
				else:
					if grid[next_y][next_x].isalpha():
						if curr_pos != start_pos:
							portal = get_portal_name(next_x, next_y, grid)
							ends[portal] = (curr_dist + 1, curr_pos)
					else:
						visited[next_pos] = curr_dist + 1
						to_visit.append(next_pos)

	return ends


def get_portal(portal_name, grid):
	letter_1_points = []
	for i in range(len(grid)):
		for j in range(len(grid[i])):
			if grid[i][j] == portal_name[0]:
				letter_1_points.append((j, i))

	portal_points = []

	for p in letter_1_points:
		if p[0] < len(grid[p[1]]) - 1 and \
				grid[p[1]][p[0] + 1] == portal_name[1]:
			portal_points.append([p, (p[0] + 1, p[1])])
		elif p[1] < len(grid) - 1 and \
				grid[p[1] + 1][p[0]] == portal_name[1]:
			portal_points.append([p, (p[0], p[1] + 1)])

	portal_ends = []

	for p in portal_points:
		if p[0][0] == p[1][0]:  # vertical
			if p[0][1] > 0 and \
					grid[p[0][1] - 1][p[0][0]] == ".":
				portal_ends.append((p[0][0], p[0][1] - 1))
			elif p[1][1] < len(grid) - 1 and \
					grid[p[1][1] + 1][p[1][0]] == ".":
				portal_ends.append((p[1][0], p[1][1] + 1))
		elif p[0][1] == p[1][1]:  # horizontal
			if p[0][0] > 0 and \
					grid[p[0][1]][p[0][0] - 1] == ".":
				portal_ends.append((p[0][0] - 1, p[0][1]))
			elif p[1][0] < len(grid[0]) and \
					grid[p[1][1]][p[1][0] + 1] == ".":
				portal_ends.append((p[1][0] + 1, p[1][1]))

	return portal_ends


start = get_portal("AA", maze)[0]
end = get_portal("ZZ", maze)[0]

print("Start: ", start)
print("End: ", end)
print()

portals_to_check = deque()
visited = []
visited.append(dict())

path_start = bfs(start, maze)
for k, v in path_start.items():
	data = (k, v[0], v[1], 0)
	portals_to_check.append(data)

while len(portals_to_check) > 0:
	curr_data = portals_to_check.popleft()
	portal = curr_data[0]
	portal_ends = get_portal(portal, maze)
	portal_ends.remove(curr_data[2])

	if len(portal_ends) > 0:
		visited[curr_data[3]][(portal, portal_ends[0])] = curr_data[1]

		path = bfs(portal_ends[0], maze, curr_data[1])
		first_set = False
		for i, p in enumerate(path.items()):
			k = p[0]
			v = p[1]

			if len(path) <= 1:
				data = (k, v[0], v[1], curr_data[3])

			if not first_set:
				data = (k, v[0], v[1], curr_data[3])
				first_set = True
			else:
				visited.append(dict())
				data = (k, v[0], v[1], len(visited) - 1)

			in_visited = False
			for j, d in enumerate(visited):
				if (k, v[1]) in d:
					in_visited = True

					if v[0] < visited[j][(k, v[1])]:
						visited[i][(k, v[1])] = v[0]
						portals_to_check.append(data)

			if not in_visited:
				portals_to_check.append(data)
	else:
		visited[curr_data[3]][(portal, None)] = curr_data[1]

z_dist = 1000000000000000

for i, k in enumerate(visited):
	if ("ZZ", None) in k:
		if k[("ZZ", None)] < z_dist:
			z_dist = k[("ZZ", None)]

print("Part 1: ", z_dist - 1)
print()

# part 2
