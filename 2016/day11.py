# @formatter:off
from os.path import isfile, join as path_join
from sys import path as sys_path
sys_path.insert(1, path_join(sys_path[0], '..'))
file_name = path_join('input', 'day11.txt')
def to_list(mf: object = int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]
def to_gen(mf: object = int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)
def p1(*args): ans = part1(*args); print(ans); return ans
def p2(*args): ans = part2(*args); print(ans); return ans

if not isfile(file_name):
	from aoc import get_input_file
	get_input_file()
# @formatter:on


from utils import parsefile

data = parsefile(file_name, [[None, 4, str, 0, " "], "\n"])

text = """The first floor contains a hydrogen-compatible microchip and a lithium-compatible microchip.
The second floor contains a hydrogen generator.
The third floor contains a lithium generator.
The fourth floor contains nothing relevant."""

# data = parse(text, [[None, 4, str, 0, " "], "\n"])

floors = []
all_items = []

for f in data[:-1]:
	floor = []

	for i in range(len(f)):
		if f[i].rstrip(".,") == "generator" or f[i].rstrip(".,") == "microchip":
			is_generator = f[i].rstrip(".,") == "generator"
			gen_initial = "G" if is_generator else "M"
			name = f[i - 1].split("-")[0]
			initial = name[0].upper()
			floor.append((name, gen_initial))
			all_items.append((name, gen_initial))

	floors.append(floor)

floors.append([])

all_items = list(all_items)

floor_count = len(floors)

"""
floors
AG + AM = fine
AG + BG = fine
AM + BM = fine
AG + BM = BM fried
AM + AG + BM = BM fried

lift
P + M = fine
P + G = fine
P + G + G = fine
P + M + M = fine
P + AM + AG = fine
P + AM + BG = fried
"""


class State:
	__slots__ = ["floors_", "lift_pos"]

	def __init__(self, floors_, lift_pos: int = 0):
		self.floors_ = [floor.copy() for floor in floors_]
		self.lift_pos = lift_pos

	@staticmethod
	def from_raw(floors_, lift_pos: int = 0):
		s = State(floors_, lift_pos)
		return s

	def __hash__(self):
		return hash((tuple(map(tuple, map(sorted, self.floors_))), self.lift_pos))

	def __eq__(self, other):
		return self.lift_pos == other.lift_pos and list(map(sorted, self.floors_)) == list(map(sorted, other.floors_))

	def __copy__(self):
		return State(self.floors_, self.lift_pos)

	def __repr__(self):
		return repr(self.lift_pos) + ": " + repr(self.floors_)

	def move_gen(self, adj_floors):
		curr_floor = self.floors_[self.lift_pos]

		next_s = []

		for v in curr_floor:
			if v[1] == "G":
				can_move_out = False
				# only move generator out of room if either:
				#       its chip is not in room
				#       its chip is in room and no other generator in room
				chip = (v[0], "M")
				if chip not in curr_floor:
					can_move_out = True
				elif chip in curr_floor and all(ob == v or ob[1] == "M" for ob in curr_floor):
					can_move_out = True

				if can_move_out:
					for f in adj_floors:
						# only move generator into room:
						#       where all chips have their own generator
						target_floor = self.floors_[f]
						if all((ob[0], "G") in target_floor for ob in target_floor if ob[1] == "M"):
							# create new state
							s = State(self.floors_, self.lift_pos)
							s.lift_pos = f
							s.floors_[self.lift_pos].remove(v)
							s.floors_[f].append(v)
							next_s.append(s)

		return next_s

	def move_chip(self, adj_floors):
		curr_floor = self.floors_[self.lift_pos]

		next_s = []

		for v in curr_floor:
			if v[1] == "M":
				# chip can move out of any room

				for f in adj_floors:
					# only move chip into room if either:
					#       no generators in room
					#       its generator in room
					target_floor = self.floors_[f]
					can_move_into = False

					if all(ob[1] == "M" for ob in target_floor):
						can_move_into = True
					elif (v[0], "G") in target_floor:
						can_move_into = True

					if can_move_into:
						# create new state
						s = State(self.floors_, self.lift_pos)
						s.lift_pos = f
						s.floors_[self.lift_pos].remove(v)
						s.floors_[f].append(v)
						next_s.append(s)

		return next_s

	def move_gen_gen(self, adj_floors):
		curr_floor = self.floors_[self.lift_pos]

		next_s = []

		cfl = list(curr_floor)
		cfl_len = len(cfl)

		for i in range(0, cfl_len - 1):
			v1 = cfl[i]
			for j in range(i + 1, cfl_len):
				v2 = cfl[j]
				if v1 != v2 and v1[1] == "G" and v2[1] == "G":
					can_move_out = False
					# can only move both generators out:
					#       if either chip is in room, no other generators
					#       both its chips not in room
					if (v1 in curr_floor or v2 in curr_floor) and all(
							ob == v1 or ob == v2 or ob[1] == "M" for ob in curr_floor):
						can_move_out = True
					elif (v1[0], "M") not in curr_floor and (v2[0], "M") not in curr_floor:
						can_move_out = True

					if can_move_out:
						for f in adj_floors:
							# only move generators into room:
							#       where all chips will have their own generators
							target_floor = self.floors_[f]
							if all((ob[0], "G") in target_floor or ob[0] == v1[0] or ob[0] == v2[0] for ob in
							       target_floor if ob[1] == "M"):
								# create new state
								s = State(self.floors_, self.lift_pos)
								s.lift_pos = f
								s.floors_[self.lift_pos].remove(v1)
								s.floors_[self.lift_pos].remove(v2)
								s.floors_[f].append(v1)
								s.floors_[f].append(v2)
								next_s.append(s)

		return next_s

	def move_chip_chip(self, adj_floors):
		curr_floor = self.floors_[self.lift_pos]

		next_s = []

		cfl = list(curr_floor)
		cfl_len = len(cfl)

		for i in range(0, cfl_len - 1):
			v1 = cfl[i]
			for j in range(i + 1, cfl_len):
				v2 = cfl[j]
				if v1 != v2 and v1[1] == "M" and v2[1] == "M":
					# chip can move out of any room

					for f in adj_floors:
						# only move chips into room if either:
						#       no generators in room
						#       both its generators in room
						target_floor = self.floors_[f]
						can_move_into = False

						if all(ob[1] == "M" for ob in target_floor):
							can_move_into = True
						elif (v1[0], "G") in target_floor and (v2[0], "G") in target_floor:
							can_move_into = True

						if can_move_into:
							# create new state
							s = State(self.floors_, self.lift_pos)
							s.lift_pos = f
							s.floors_[self.lift_pos].remove(v1)
							s.floors_[self.lift_pos].remove(v2)
							s.floors_[f].append(v1)
							s.floors_[f].append(v2)
							next_s.append(s)

		return next_s

	def move_gen_chip(self, adj_floors):
		curr_floor = self.floors_[self.lift_pos]

		next_s = []

		for v1 in curr_floor:
			for v2 in curr_floor:
				if v1[0] == v2[0] and v1[1] == "M" and v2[1] == "G":
					# chip can move out of any room

					for f in adj_floors:
						# only move generators into room:
						#       where all chips have their own generators
						target_floor = self.floors_[f]
						if all((ob[0], "G") in target_floor for ob in target_floor if ob[1] == "M"):
							# create new state
							s = State(self.floors_, self.lift_pos)
							s.lift_pos = f
							s.floors_[self.lift_pos].remove(v1)
							s.floors_[self.lift_pos].remove(v2)
							s.floors_[f].append(v1)
							s.floors_[f].append(v2)
							next_s.append(s)

		return next_s

	def get_next_states(self):
		adj_floors = []
		if self.lift_pos < floor_count - 1:
			adj_floors.append(self.lift_pos + 1)
		if self.lift_pos > 0:
			adj_floors.append(self.lift_pos - 1)

		next_states = []

		# get the moves
		next_states += self.move_chip(adj_floors)
		next_states += self.move_gen(adj_floors)
		next_states += self.move_gen_gen(adj_floors)
		next_states += self.move_chip_chip(adj_floors)
		next_states += self.move_gen_chip(adj_floors)

		return next_states


def bfs(start_state: State, end_state: State):
	to_check = [start_state]
	end_states = []

	dists = {start_state: 0}

	while len(to_check) > 0:
		curr_state = to_check.pop(0)
		curr_dist = dists[curr_state]

		next_states = curr_state.get_next_states()

		for state in next_states:
			if state == end_state:
				end_states.append((state, curr_dist + 1))
				return curr_dist + 1
			else:
				if state not in dists:
					to_check.append(state)
					dists[state] = curr_dist + 1
				elif curr_dist + 1 < dists[state]:
					to_check.append(state)
					dists[state] = curr_dist + 1


def part1():
	start = [floor.copy() for floor in floors]
	end = [[] for _ in range(floor_count)]
	end[-1] = all_items

	start_state = State.from_raw(start, 0)
	end_state = State.from_raw(end, 3)

	steps = bfs(start_state, end_state)
	return steps


def part2():
	new_floors = [floor.copy() for floor in floors]
	new_all_items = all_items.copy()

	items = [("elerium", "G"), ("elerium", "M"), ("dilithium", "G"), ("dilithium", "M")]
	new_floors[0].extend(items)
	new_all_items.extend(items)

	start = [floor.copy() for floor in new_floors]
	end = [[] for _ in range(floor_count)]
	end[-1] = new_all_items

	start_state = State.from_raw(start, 0)
	end_state = State.from_raw(end, 3)

	steps = bfs(start_state, end_state)
	return steps


p1()
p2()
