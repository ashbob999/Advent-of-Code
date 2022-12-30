# @formatter:off
from os.path import isfile, join as path_join
from sys import path as sys_path
sys_path.insert(1, path_join(sys_path[0], '..'))
file_name = path_join('input', 'day17.txt')
def to_list(mf: object = int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]
def to_gen(mf: object = int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)
def p1(*args): ans = part1(*args); print(ans); return ans
def p2(*args): ans = part2(*args); print(ans); return ans

if not isfile(file_name):
	from aoc import get_input_file
	get_input_file(session_path=['..', '.env'])
# @formatter:on

from utils import parsefile

moves = parsefile(file_name, None)
movesa = ">>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>"

shapes = {
	0:[(i, 0) for i in range(4)],
	1:[(0, 1), (1, 0), (1, 1), (1, 2), (2, 1)],
	2:[(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)],
	3:[(0, i) for i in range(4)],
	4:[(i, j) for i in range(2) for j in range(2)]
}

shape_width = {
	0: 4,
	1: 3,
	2: 3,
	3: 1,
	4: 2
}

def gen_move():
	while True:
		for m in moves:
			#print("move", m)
			yield m
			
class gen_move():
	def __init__(self):
		self.i = 0
		
	def __next__(self):
		self.i += 1
		self.i %= len(moves)
		return moves[self.i]
			
def do_move(grid, dir, pos, shape):
	if dir == "<":
		diff = (-1, 0)
	elif dir == ">":
		diff = (1, 0)
	elif dir == "v":
		diff = (0, -1)
		
	new_pos = (pos[0] + diff[0], pos[1] + diff[1])
	#print("pos", pos, new_pos, dir)
	for p in shapes[shape]:
		np = (new_pos[0] + p[0], new_pos[1] + p[1])
		#print(p, np)
		if np[0] < 0 or np[0] >= 7:
			#print(shape, pos, dir, np, "hit wall")
			return False, pos
			
		if np[1] < 0 and dir == "v":
			#print(shape, pos, dir, "hit floor")
			return True, None
		
		if np in grid:
			if dir == "v":
				#print(shape, pos, dir, "hit shape")
				return True, None
			else:
				return False, pos
				
	return False, new_pos # not at bottom

grid = set()
#for i in range(7): # bottom
#	grid.add((0, i))



def part1():
	g = grid.copy()
	gm = gen_move()
	
	sp = (2, 3)
	max_y = -1
	for i in range(2022):
		#print(i)
		shape = i % 5
		pos = (2, max_y + 4)
		#print("new shape", pos)
		while True:
			res = do_move(g, next(gm), pos, shape)
			if res[0]: # stopped
				for p in shapes[shape]:
					np = (pos[0]+p[0], pos[1]+p[1])
					if np in grid:
						print("error")
						quit()
					g.add(np)
			
				break
				
			pos = res[1]
			#print(pos)
			res = do_move(g, "v", pos, shape)
			if res[0]: # stopped
				for p in shapes[shape]:
					np = (pos[0]+p[0], pos[1]+p[1])
					if np in grid:
						print("error")
						quit()
					g.add(np)
			
				break
				
			pos = res[1]
			#print(pos)
		
		#print(grid)
		max_y = max(map(lambda x: x[1], g))
		
	return max_y +1


def find_cycle():
	g = grid.copy()
	gm = gen_move()
	
	cycle_data = {}
	
	sp = (2, 3)
	max_y = -1
	for i in range(10000):
		print(i)
		shape = i % 5
		pos = (2, max_y + 4)
		#print("new shape", pos)
		while True:
			res = do_move(g, next(gm), pos, shape)
			if res[0]: # stopped
				for p in shapes[shape]:
					np = (pos[0]+p[0], pos[1]+p[1])
					if np in grid:
						print("error")
						quit()
					g.add(np)
			
				break
				
			pos = res[1]
			#print(pos)
			res = do_move(g, "v", pos, shape)
			if res[0]: # stopped
				for p in shapes[shape]:
					np = (pos[0]+p[0], pos[1]+p[1])
					if np in grid:
						print("error")
						quit()
					g.add(np)
			
				break
				
			pos = res[1]
			#print(pos)
		
		#print(grid)
		max_y = max(map(lambda x: x[1], g))
		
		if shape == 0:
			height = max_y
			dat = (
		
		
	return max_y +1

def part2():
	cycle = find_cycle()


#p1()
p2()
