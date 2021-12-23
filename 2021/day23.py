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

rooms =[[None, None],
		[None, None],
		[None, None],
		[None, None]]

hallway_pos = [(1, 1), (1, 2), (1, 4), (1, 6), (1, 8), (1, 10), (1, 11)]
hallway = [c if c=="#" else None for c in grid[1]]

cost = {"A":1, "B":10, "C":100, "D":1000}

correct_rooms = {v:i for i, v in enumerate(["A", "B", "C", "D"])}

creatures = {}
fc = set()

for y in range(2, 4):
	for x in range(3, 10, 2):
		if grid[y][x] in fc:
			creatures[grid[y][x]+"2"] = (x, y)
		else:
			creatures[grid[y][x]+"1"] = (x, y)
			fc.add(grid[y][x])

for cr, pos in creatures.items():
	rx = (pos[0]-3)//2
	ry = pos[1] -2
	rooms[rx][ry] = cr

move_counts = {k:0 for k in creatures.keys()}

scores = [10000000000000000000]

def dc(list2d):
	return [v[:] for v in list2d]

def check_rooms(rooms):
	if rooms[0][0] is not None and rooms[0][1] is not None and rooms[0][0][0] == rooms[0][1][0]:
		if rooms[1][0] is not None and rooms[1][1] is not None and rooms[1][0][0] == rooms[1][1][0]:
				if rooms[2][0] is not None and  rooms[2][1] is not None and rooms[2][0][0] == rooms[2][1][0]:
					if rooms[3][0] is not None and  rooms[3][1] is not None and rooms[3][0][0] == rooms[3][1][0]:
						return True
	return False

def get_dist(rooms, hallway, creatures, creature, pos, for_room):
	dist = 0
	cp = creatures[creature]
	
	for x in range(min(pos[0], cp[0]), max(pos[0], cp[0]) +1):
		if hallway[x] in (None, creature):
			dist += 1
		else:
			return 0
	
	#print("dist", dist)
	
	rxp = (pos[0] -3) // 2
	rxc = (cp[0] -3) // 2
	py = pos[1] - (2 if for_room else 0)
	cy = cp[1] - (0 if for_room else 2)
	
	max_ry = py-2 if for_room else cy-2
	#print("max_ry", max_ry)
	
	#print("adj", py, cy)
	
	#print(rxp, rxc, for_room)
	for y in range(0, max_ry+1):
		#print("y", y)
		#print(creature)
		#print(rooms)
		if for_room and rooms[rxp][y] in (None, creature):
			dist += 1
		elif not for_room and rooms[rxc][y] in (None, creature):
			dist += 1
		else:
			#print("here")
			return 0
		
	return dist

#print(get_dist(rooms, hallway, creatures, "D1", (11, 1), False))
#assert get_dist(rooms, hallway, creatures, "D1", (11, 1), False) == 9

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

def hash(rooms, hallway):
	rooms = tuple([tuple(v) for v in rooms])
	hallway = tuple(hallway)
	return (rooms, hallway)

def h2(rooms):
	return tuple([tuple(v) for v in rooms])

def is_dest_room(x, cr):
	return correct_rooms[cr[0]] == x

def pp(rooms, hallway):
	print("#"*13)
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
	next_states = {}
	
	for cr, pos in creatures.items():
		if move_counts[cr] >= 2:
			continue
			
		if cr in hallway: # move to room
			for xp in range(3, 10, 2):
				rx = (x-3) // 2
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
						nc[cr] = (xp, fr+2)
						nmc = move_counts.copy()
						nmc[cr] += 1
						#print("move to room")
						if score+dist not in next_states:
							next_states[score+dist] = [(nr, nh, nc, nmc, score + dist)]
						else:
							next_states[score+dist].append((nr, nh, nc, nmc, score + dist))
		else:
			for xp in range(1, 12, 1):
				if xp in (3, 5, 7, 9):
					continue
				rx = (pos[0] -3) // 2
				dist = get_dist(rooms, hallway, creatures, cr, (xp, 1), False)
				#print(cr, pos, (xp, 1), dist)
				if dist > 0:
					dist *= cost[cr[0]]

					nr = dc(rooms)
					nr[rx][pos[1]-2] = None
					nh = hallway[:]
					nh[xp] = cr
					nc = creatures.copy()
					nc[cr] = (xp, 1)
					nmc = move_counts.copy()
					nmc[cr] += 1
					#print("move to hallway")
					if score+dist not in next_states:
						next_states[score+dist] = [(nr, nh, nc, nmc, score + dist)]
					else:
						next_states[score+dist].append((nr, nh, nc, nmc, score + dist))

	return next_states

room_to_hall = {}
mem_states = {}

def get_scores(rooms, hallway, creatures, move_counts, score):
	#print(scores, score)
	#print(rooms)
	
	h = h2(rooms)
	if h in mem_states:
		if mem_states[h] < score:
			#print("less score")
			return
	else:
		mem_states[h] = score
		room_to_hall[h]= hallway

	pp(rooms, hallway)

	if check_rooms(rooms):
		scores.append(score)
		return
		
	for cr, pos in creatures.items():
		if move_counts[cr] >= 2:
			continue
			
		if cr in hallway: # move to room
			for xp in range(3, 10, 2):
				rx = (x-3) // 2
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
						nc[cr] = (xp, fr+2)
						nmc = move_counts.copy()
						nmc[cr] += 1
						print("move to room")
						get_scores(nr, nh, nc, nmc, score + dist)
		else:
			for xp in range(1, 12, 1):
				if xp in (3, 5, 7, 9):
					continue
				rx = (pos[0] -3) // 2
				dist = get_dist(rooms, hallway, creatures, cr, (xp, 1), False)
				#print(cr, pos, (xp, 1), dist)
				if dist > 0:
					dist *= cost[cr[0]]

					nr = dc(rooms)
					nr[rx][pos[1]-2] = None
					nh = hallway[:]
					nh[xp] = cr
					nc = creatures.copy()
					nc[cr] = (xp, 1)
					nmc = move_counts.copy()
					nmc[cr] += 1
					print("move to hallway")
					get_scores(nr, nh, nc, nmc, score + dist)


def part1():
	for k, v in get_next_states(rooms, hallway, creatures, move_counts, 0).items():
		print(k)
		for s in v:
			pp(s[0], s[1])

	#get_scores(rooms, hallway, creatures, move_counts, 0)
	
	return min(scores)


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
"""
