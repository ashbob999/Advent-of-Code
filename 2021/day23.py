from os.path import isfile, join as path_join
from sys import path as sys_path
sys_path.insert(1, path_join(sys_path[0], '..'))
file_name = path_join('input', 'day23.txt')
def to_list(mf: object = int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]
def to_gen(mf: object = int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)
def p1(*args): ans = part1(*args); print(ans); return ans
def p2(*args): ans = part2(*args); print(ans); return ans

if not isfile(file_name):
	from aoc import get_input_file

	get_input_file(session_path=['..', '.env'])

from utils import parsefile

grid = parsefile(file_name, [str, "\n"])

grid = """#############
#...........#
###B#C#B#D###
  #A#D#C#A#
  #########""".split("\n")

rooms = [[None, None],
         [None, None],
         [None, None],
         [None, None]]


class Rooms:
	def __init__(self):
		self.rooms = [[None, None],
		              [None, None],
		              [None, None],
		              [None, None]]

	def load(self, creatures):
		for creature in creatures.keys():
			for pos in creatures[creature]:
				room_x = (pos[0] - 3) // 2
				room_y = pos[1] - 2
				self.rooms[room_x][room_y] = creature

	def check_correct(self):
		if self.rooms[0][0] == "A" and self.rooms[0][1] == "A":
			if self.rooms[1][0] == "B" and self.rooms[1][1] == "B":
				if self.rooms[2][0] == "C" and self.rooms[2][1] == "C":
					if self.rooms[3][0] == "D" and self.rooms[3][1] == "D":
						return True
		return False

	def correct_room(self, x, y, creature_type):
		room_x = (x - 3) // 2
		# print(room_x)
		return {0: "A", 1: "B", 2: "C", 3: "D"}[room_x] == creature_type

	def can_fit(self, x, y, creature_type):
		if self.correct_room(x, y, creature_type):
			room_x = (x - 3) // 2
			return all(v in (creature_type, None) for v in self.rooms[room_x])
		return False

	def global_pos_value(self, x: int, y: int):
		room_x = (x - 3) // 2
		room_y = y - 2
		# print("global_pos_value", room_x, room_y, x, y)
		return self.rooms[room_x][room_y]

	def local_pos_value(self, x: int, y: int):
		return self.rooms[y][x]

	def set_pos(self, x: int, y: int, value):
		room_x = (x - 3) // 2
		room_y = y - 2
		# print("set_pos", room_x, room_y, value)
		self.rooms[room_x][room_y] = value

	def __lt__(self, other):
		return sum([1 for y in range(2) for x in range(4) if self.rooms[x][y] is not None]) < sum(
			[1 for y in range(2) for x in range(4) if other.rooms[x][y] is not None])

	def copy(self):
		tmp = Rooms()
		tmp.rooms = [[v for v in row] for row in self.rooms]
		return tmp

	def __repr__(self):
		return "Rooms Object:\t" + repr(self.rooms) + "\n"

	def __hash__(self):
		return hash(tuple([tuple(row) for row in self.rooms]))

	def __eq__(self, other):
		return self.rooms == other.rooms


class Grid:
	cost = {"A": 1, "B": 10, "C": 100, "D": 1000}

	def __init__(self):
		self.rooms = Rooms()
		self.hallway = [None] * 11

		self.creature_pos = {}
		self.grid = []

		self.score = 0
		self.weight = 0

	def load(self, inp: str):
		self.grid = [[c for c in row.ljust(13, " ")] for row in inp.split("\n")]
		# print("grid", self.grid)

		for y in range(2, 4):
			for x in range(3, 10, 2):
				if self.grid[y][x] in self.creature_pos:
					self.creature_pos[self.grid[y][x]].append((x, y))
				else:
					self.creature_pos[self.grid[y][x]] = [(x, y)]

		self.rooms.load(self.creature_pos)

	def is_hallway(self, x, y):
		if y == 1 and 0 < x < 12:
			return True
		return False

	def is_room(self, x, y):
		if 1 < y < 4 and (x - 3) % 2 == 0:
			return True
		return False

	def copy(self):
		tmp = Grid()
		tmp.rooms = self.rooms.copy()
		tmp.grid = [[v for v in row] for row in self.grid]
		tmp.hallway = [v for v in self.hallway]
		tmp.creature_pos = {k: [i for i in v] for k, v in self.creature_pos.items()}
		tmp.score = self.score
		tmp.weight = self.weight
		return tmp

	def set_hallway_pos(self, x: int, value):
		self.hallway[x - 1] = value

	def move_pos(self, old, new, creature_type):
		# print("move", old, new, creature_type)
		if self.is_room(*old):
			self.rooms.set_pos(old[0], old[1], None)
		elif self.is_hallway(*old):
			self.set_hallway_pos(old[0], None)

		if self.is_room(*new):
			self.rooms.set_pos(*new, creature_type)
		elif self.is_hallway(*new):
			self.set_hallway_pos(new[0], creature_type)

		self.creature_pos[creature_type].remove(old)
		self.creature_pos[creature_type].append(new)

	def get_hallway_points(self, x: int, y: int):
		points = {}
		# print("hp", x, y)
		# check to the left
		nx = x - 1
		while nx > 0:
			if self.hallway[nx - 1] is not None:
				break

			points[(nx, y)] = x - nx

			nx -= 1

		# check to the right
		nx = x + 1
		while nx < 12:
			if self.hallway[nx - 1] is not None:
				break

			points[(nx, y)] = nx - x

			nx += 1

		return points

	def get_search_path(self, creature_type: str, x: int, y: int):
		points = {}

		# room -> hallway (done)
		# hallway -> correct room (done)
		# room -> room (done)

		# only leave correct room if contains others below

		from_room = False

		weight = 0

		if self.is_room(x, y):
			from_room = True

			# only leave correct room if contains others below
			if self.rooms.can_fit(x, y, creature_type):
				return {}

			# print("is room", x, y)
			# print(self.hallway)
			if y == 2:
				if self.hallway[x] is not None:
					return {}
				y -= 1
				weight = 1
			elif y == 3:
				if self.rooms.global_pos_value(x, y - 1) is not None:  # can't get out of room
					# print("cant leave")
					return {}
				y -= 1
				if self.hallway[x] is not None:
					# print("hallway blocked")
					return {}
				y -= 1
				weight = 2

		# print(creature_type, x, y)

		hp = self.get_hallway_points(x, y)

		for p, w in hp.items():
			# check if point is above a room
			if 2 < p[0] < 10 and (p[0] - 3) % 2 == 0:# and not from_room:
				# print(p)
				# is it the correct room
				if self.rooms.correct_room(p[0], p[1], creature_type) and self.rooms.can_fit(p[0], p[1], creature_type):
					# can we put point in room
					top_free = self.rooms.global_pos_value(p[0], 2) is None
					bottom_free = self.rooms.global_pos_value(p[0], 3) is None and top_free
					if bottom_free:
						points[(p[0], 3)] = w + 2 + weight
					elif top_free:
						points[(p[0], 2)] = w + 1 + weight
			else:
				if from_room:
					points[p] = w + weight

		return points

	def get_next_states(self):
		next_states = []

		for creature_type in self.creature_pos.keys():
			for creature_pos in self.creature_pos[creature_type]:
				poss_points = self.get_search_path(creature_type, *creature_pos)
				# print(creature_pos, poss_points)
				for pos, weight in poss_points.items():
					grid_tmp = self.copy()
					# print(creature_pos, pos)
					grid_tmp.move_pos(creature_pos, pos, creature_type)
					grid_tmp.score += weight * cost[creature_type]
					grid_tmp.weight = weight * cost[creature_type]
					# print(grid_tmp)
					next_states.append(grid_tmp)

		return next_states

	def __repr__(self):
		s = "Grid Object:\n"
		s += "\t" + repr(self.hallway) + "\n"
		s += "\t" + repr(self.rooms) + "\n"

		return s

	def __hash__(self):
		creature_pos_tuple = tuple([(k, tuple(sorted(v))) for k, v in self.creature_pos.items()])
		hallway_tuple = tuple(self.hallway)
		room_tuple = hash(self.rooms)

		return hash((creature_pos_tuple, hallway_tuple, room_tuple))

	def __eq__(self, other):
		creature_pos_equal = all(
			sorted(self.creature_pos[k]) == sorted(other.creature_pos[k]) for k in self.creature_pos.keys())
		hallway_equal = self.hallway == other.hallway
		room_equal = self.rooms == other.rooms
		return creature_pos_equal and hallway_equal and room_equal

	def __lt__(self, other):
		return self.score < other.score and self.rooms < other.rooms


def test_p1():
	g = Grid()
	g.load(parsefile(file_name, None))
	# print(g.rooms.rooms)
	ns = g.get_next_states()
	print("\n\n\nnext states\n")
	print(ns[0])
	print("next state")
	nss = ns[0].get_next_states()
	# print(nss)
	print(len(nss))
	print(len(ns))
	# for n in ns:
	# 	print(n, hash(n))

	return


hallway_pos = [(1, 1), (1, 2), (1, 4), (1, 6), (1, 8), (1, 10), (1, 11)]
hallway = [c if c == "#" else None for c in grid[1]]
cost = {"A": 1, "B": 10, "C": 100, "D": 1000}

correct_rooms = {v: i for i, v in enumerate(["A", "B", "C", "D"])}

creatures = {}
fc = set()

for y in range(2, 4):
	for x in range(3, 10, 2):
		if grid[y][x] in fc:
			creatures[grid[y][x] + "2"] = (x, y)
		else:
			creatures[grid[y][x] + "1"] = (x, y)
			fc.add(grid[y][x])

for cr, pos in creatures.items():
	rx = (pos[0] - 3) // 2
	ry = pos[1] - 2
	rooms[rx][ry] = cr

move_counts = {k: 0 for k in creatures.keys()}

scores = [10000000000000000000]


def dc(list2d):
	return [v[:] for v in list2d]


def check_rooms(rooms):
	if rooms[0][0] is not None and rooms[0][1] is not None and rooms[0][0][0] == rooms[0][1][0]:
		if rooms[1][0] is not None and rooms[1][1] is not None and rooms[1][0][0] == rooms[1][1][0]:
			if rooms[2][0] is not None and rooms[2][1] is not None and rooms[2][0][0] == rooms[2][1][0]:
				if rooms[3][0] is not None and rooms[3][1] is not None and rooms[3][0][0] == rooms[3][1][0]:
					return True
	return False


def get_dist(rooms, hallway, creatures, creature, pos, for_room):
	dist = 0
	cp = creatures[creature]

	for x in range(min(pos[0], cp[0]), max(pos[0], cp[0]) + 1):
		if hallway[x] in (None, creature):
			dist += 1
		else:
			return 0

	# print("dist", dist)

	rxp = (pos[0] - 3) // 2
	rxc = (cp[0] - 3) // 2
	py = pos[1] - (2 if for_room else 0)
	cy = cp[1] - (0 if for_room else 2)

	max_ry = py - 2 if for_room else cy - 2
	# print("max_ry", max_ry)

	# print("adj", py, cy)

	# print(rxp, rxc, for_room)
	for y in range(0, max_ry + 1):
		# print("y", y)
		# print(creature)
		# print(rooms)
		if for_room and rooms[rxp][y] in (None, creature):
			dist += 1
		elif not for_room and rooms[rxc][y] in (None, creature):
			dist += 1
		else:
			# print("here")
			return 0

	return dist


# print(get_dist(rooms, hallway, creatures, "D1", (11, 1), False))
# assert get_dist(rooms, hallway, creatures, "D1", (11, 1), False) == 9

def get_top(rooms, x):
	if rooms[x][1] is not None:
		return rooms[x][1]
	elif rooms[x][0] is not None:
		return rooms[x][1]
	else:
		return None

def room_free(rooms, x, creature):
	if rooms[x][0] is None:
		return 0
	elif rooms[x][1] is None and rooms[x][0][0] == creature[0]:
		return 1
	else:
		return None


def custom_hash(rooms, hallway):
	rooms = tuple([tuple(v) for v in rooms])
	hallway = tuple(hallway)
	return (rooms, hallway)


def h2(rooms):
	return tuple([tuple(v) for v in rooms])


def is_dest_room(x, cr):
	return correct_rooms[cr[0]] == x


def pp(rooms, hallway):
	print("#" * 13)
	print("".join(v[0] if v is not None else "." for v in hallway))
	print("###", end="")
	for i in range(4):
		if rooms[i][0] is None:
			print(".#", end="")
		else:
			print(rooms[i][0][0] + "#", end="")
	print("##")
	print("  #", end="")
	for i in range(4):
		if rooms[i][1] is None:
			print(".#", end="")
		else:
			print(rooms[i][1][0] + "#", end="")
	print("")
	print("  #########")
	print()


def get_next_states(rooms, hallway, creatures, move_counts, score):
	next_states = []

	for cr, pos in creatures.items():
		if move_counts[cr] >= 2:
			continue

		if cr in hallway:  # move to room
			for xp in range(3, 10, 2):
				rx = (x - 3) // 2
				if not is_dest_room(rx, cr):
					continue
				fr = room_free(rooms, rx, cr)
				if fr is not None:
					dist = get_dist(rooms, hallway, creatures, cr, (x, fr), True)
					if dist > 0:
						dist *= cost[cr[0]]
						nr = dc(rooms)
						nr[rx][fr] = cr
						nh = hallway[:]
						nh[pos[0]] = None
						nc = creatures.copy()
						nc[cr] = (xp, fr + 2)
						nmc = move_counts.copy()
						nmc[cr] += 1
						# print("move to room")
						next_states.append((nr, nh, nc, nmc, score + dist))
		else:
			for xp in range(1, 12, 1):
				if xp in (3, 5, 7, 9):
					continue
				rx = (pos[0] - 3) // 2
				dist = get_dist(rooms, hallway, creatures, cr, (xp, 1), False)
				# print(cr, pos, (xp, 1), dist)
				if dist > 0:
					dist *= cost[cr[0]]

					nr = dc(rooms)
					nr[rx][pos[1] - 2] = None
					nh = hallway[:]
					nh[xp] = cr
					nc = creatures.copy()
					nc[cr] = (xp, 1)
					nmc = move_counts.copy()
					nmc[cr] += 1
					# print("move to hallway")
					next_states.append((nr, nh, nc, nmc, score + dist))

	return next_states


room_to_hall = {}
mem_states = {}


def get_scores(rooms, hallway, creatures, move_counts, score):
	# print(scores, score)
	# print(rooms)

	h = h2(rooms)
	if h in mem_states:
		if mem_states[h] < score:
			# print("less score")
			return
	else:
		mem_states[h] = score
		room_to_hall[h] = hallway

	pp(rooms, hallway)

	if check_rooms(rooms):
		scores.append(score)
		return

	for cr, pos in creatures.items():
		if move_counts[cr] >= 2:
			continue

		if cr in hallway:  # move to room
			for xp in range(3, 10, 2):
				rx = (x - 3) // 2
				if not is_dest_room(rx, cr):
					continue
				fr = room_free(rooms, rx, cr)
				if fr is not None:
					dist = get_dist(rooms, hallway, creatures, cr, (x, fr), True)
					if dist > 0:
						dist *= cost[cr[0]]
						nr = dc(rooms)
						nr[rx][fr] = cr
						nh = hallway[:]
						nh[pos[0]] = None
						nc = creatures.copy()
						nc[cr] = (xp, fr + 2)
						nmc = move_counts.copy()
						nmc[cr] += 1
						print("move to room")
						get_scores(nr, nh, nc, nmc, score + dist)
		else:
			for xp in range(1, 12, 1):
				if xp in (3, 5, 7, 9):
					continue
				rx = (pos[0] - 3) // 2
				dist = get_dist(rooms, hallway, creatures, cr, (xp, 1), False)
				# print(cr, pos, (xp, 1), dist)
				if dist > 0:
					dist *= cost[cr[0]]

					nr = dc(rooms)
					nr[rx][pos[1] - 2] = None
					nh = hallway[:]
					nh[xp] = cr
					nc = creatures.copy()
					nc[cr] = (xp, 1)
					nmc = move_counts.copy()
					nmc[cr] += 1
					print("move to hallway")
					get_scores(nr, nh, nc, nmc, score + dist)


from heapq import *


def hf(start):
	return 0
	return abs(start[0]) + abs(start[1])


def create_path(came_from, current):
	tp = [current]
	while current in came_from:
		current = came_from[current]
		tp.append(current)

	return tp[::-1]


def a_star(start: Grid):
	found_grids = []

	in_heap = set()
	heap = []
	heappush(heap, start)
	in_heap.add(start)

	came_from = {}

	g_score = {start: 0}

	while len(heap) > 0:
		print("heap len", len(heap), len(g_score))
		curr: Grid = heappop(heap)
		curr_dist: int = curr.score
		in_heap.remove(curr)

		if curr.rooms.check_correct():
			# print("ended")
			# return g_score, g_score[curr], create_path(came_from, curr)
			found_grids.append(curr)

		for next_state in curr.get_next_states():
			tg_score = g_score[curr] + next_state.weight
			if next_state not in g_score or tg_score < g_score[next_state]:
				came_from[next_state] = curr

				g_score[next_state] = tg_score

				if next_state not in in_heap:
					# print(next_state[:-1])
					heappush(heap, next_state)
					in_heap.add(next_state)

	return found_grids

from collections import deque

def search(start, trace=False):
	all_states = {start: (0, None)}
	queue = deque([start])
	while queue:
		state:Grid = queue.popleft()
		cost, prev = all_states[state]
		# print(state, cost)
		for next, next_cost in state.get_next_states():
			if next in all_states and all_states[next][0] <= cost + next_cost:
				continue
			all_states[next] = (cost + next_cost, state)
			queue.append(next)

def part1():
	# load the grid
	g = Grid()
	# g.load(parsefile(file_name, None))

	a = """#############
#...........#
###B#C#B#D###
  #A#D#C#A#
  #########"""  # 12521

	b = """#############
#...........#
###B#A#C#D###
  #A#B#C#D#
  #########"""  # 46

	c = """#############
#...........#
###C#A#B#D###
  #A#B#C#D#
  #########"""  # 646

	real = """#############
#...........#
###D#B#D#B###
  #C#A#A#C#
  #########"""  # 14627

	g.load(real)

	# test_p1()

	start = g
	# scores, score, path = a_star(start)
	found_grids = a_star(start)
	# print(len(found_grids))
	# print(found_grids)

	score = min([v.score for v  in found_grids])

	# print(scores)
	# print(path)

	return score


def part2():
	pass


p1()
p2()

"""

...........
  d b d b
  c a a c

move right b to right
..........b
  d b d _
  c a a c

b3 = 30

move right c to right
.........cb
  d b d _
  c a a _
  
c3 = 300

move right d to r4
.........cb
  d b _ _
  c a a d
  
d5 = 5000
  
move left d to r4
.........cb
  _ b _ d
  c a a d
  
d8 = 8000

move right a to left but 1
.a.......cb
  _ b _ d
  c a _ d

a7 = 7

move left c to r3
.a.......cb
  _ b _ d
  _ a c d

c8 = 800

move right c to r3
.a........b
  _ b c d
  _ a c d

c4 = 400

move left a to r1
..........b
  _ b c d
  a a c d

a3 = 3

move left b to mid
.....b....b
  _ _ c d
  a a c d

b2 = 20

move a to r1
.....b....b
  a _ c d
  a _ c d

a5 = 5

move left b to r2
..........b
  a _ c d
  a b c d

b3 = 30

move right b to r2
...........
  a b c d
  a b c d
  
b7 = 70


14665 too high
used https://amphipod.net/

part 1
14383 too low
correct 14627
14629 too high
14665 too high

part 2
44431 too high
"""
