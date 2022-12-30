# @formatter:off
from os.path import isfile, join as path_join
from sys import path as sys_path
sys_path.insert(1, path_join(sys_path[0], '..'))
file_name = path_join('input', 'day22.txt')
def to_list(mf: object = int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]
def to_gen(mf: object = int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)
def p1(*args): ans = part1(*args); print(ans); return ans
def p2(*args): ans = part2(*args); print(ans); return ans

if not isfile(file_name):
	from aoc import get_input_file
	get_input_file(session_path=['..', '.env'])
# @formatter:on

raw_grid, path = open(file_name).read().split("\n\n")

raw_grid, path = \
"""        ...#
        .#..
        #...
        ....
...#.......#
........#...
..#....#....
..........#.
        ...#....
        .....#..
        .#......
        ......#.

10R5L5R10L4R5L5""".split("\n\n")

raw_grid = [r for r in raw_grid.split("\n") if r]

width = 0
for r in raw_grid:
	width = max(width, len(r))
	
height = len(raw_grid)

grid = [[" " for x in range(width)] for y in range(height)]

for y in range(0, height):
	for x, v in enumerate(raw_grid[y]):
		if v != " ":
			grid[y][x] = v

start = [0, 0]
while grid[start[1]][start[0]] != ".":
	start[0] += 1

import re

moves = [v for v in re.split("([A-Z])", path.replace("\n", "")) if v]

dirs = ((1, 0), (0, 1), (-1, 0), (0, -1))

def part1():
	pos = start[:]
	facing = 0 # right
	
	for move in moves:
		if move[0] == "L":
			facing -= 1
			facing %= 4
		elif move[0] == "R":
			facing += 1
			facing %= 4
		else:
			count = int(move)
			dir = dirs[facing]
			for i in range(count):
				nd = [pos[0] + dir[0], pos[1] + dir[1]]
				if nd[0] < 0 or nd[0] >= width or nd[1] < 0 or nd[1] >= height \
						or grid[nd[1]][nd[0]] == " ":
					# wrap around
					tp = pos[:]
					rdir = [dir[0]*-1, dir[1]*-1]
					while 0 <= tp[0] < width and 0 <= tp[1] < height \
							and grid[tp[1]][tp[0]] != " ":
						tp = [tp[0]+rdir[0], tp[1]+rdir[1]]
					tp = [tp[0]+dir[0], tp[1]+dir[1]]
					if grid[tp[1]][tp[0]] == "#":
						break
					else:
						pos = tp
				
				elif grid[nd[1]][nd[0]] == "#":
					break
				elif grid[nd[1]][nd[0]] == " ":
					pass
				else:
					pos = nd
				
	return (pos[1]+1)*1000 + (pos[0]+1)*4 + facing

cube_size = 4
cube_faces = {
	(2, 0): 1,
	(0, 1): 2,
	(1, 2): 3,
	(2, 1): 4,
	(2, 2): 5,
	(3, 2): 6,
}


def part2():
	pos = start[:]
	facing = 0 # right
	
	for move in moves:
		if move[0] == "L":
			facing -= 1
			facing %= 4
		elif move[0] == "R":
			facing += 1
			facing %= 4
		else:
			count = int(move)
			dir = dirs[facing]
			for i in range(count):
				nd = [pos[0] + dir[0], pos[1] + dir[1]]
				if nd[0] < 0 or nd[0] >= width or nd[1] < 0 or nd[1] >= height \
						or grid[nd[1]][nd[0]] == " ":
					# wrap around on cube
					# get cube face
					face = cube_faces[(pos[0]//cube_size, pos[1]//cube_size)]
					
					if face==1 and facing==0:
						tp = (cube_size*4-1, cube_size*3-1 - pos[0] % cube_size)
						nf = 2
					elif face==1 and facing==1:
						tp = (pos[0]+1, pos[1])
						nf = 1
					elif face==1 and facing==2:
						tp = (cube_size*1 + pos[1] % cube_size, cube_size*1)
						nf = 1
					elif face==1 and facing==3:
						tp = (cube_size*1-1 - pos[, cube_siez*1)
						nf = 1
					
					elif face==2 and facing==0:
						tp = ()
						nf = 
					elif face==2 and facing==1:
						tp = ()
						nf = 
					elif face==2 and facing==2:
						tp = ()
						nf = 
					elif face==2 and facing==3:
						tp = ()
						nf = 
					
					elif face==3 and facing==0:
						tp = ()
						nf = 
					elif face==3 and facing==1:
						tp = ()
						nf = 
					elif face==3 and facing==2:
						tp = ()
						nf = 
					elif face==3 and facing==3:
						tp = ()
						nf = 
						
					elif face==4 and facing==0:
						tp = ()
						nf = 
					elif face==4 and facing==1:
						tp = ()
						nf = 
					elif face==4 and facing==2:
						tp = ()
						nf = 
					elif face==4 and facing==3:
						tp = ()
						nf = 
					
					elif face==5 and facing==0:
						tp = ()
						nf = 
					elif face==5 and facing==1:
						tp = ()
						nf = 
					elif face==5 and facing==2:
						tp = ()
						nf = 
					elif face==5 and facing==3:
						tp = ()
						nf = 
					
					elif face==6 and facing==0:
						tp = ()
						nf = 
					elif face==6 and facing==1:
						tp = ()
						nf = 
					elif face==6 and facing==2:
						tp = ()
						nf = 
					elif face==6 and facing==3:
						tp = ()
						nf = 
					
					if grid[tp[1]][tp[0]] == "#":
						break
					else:
						pos = tp
						facing = nf
					
				
				elif grid[nd[1]][nd[0]] == "#":
					break
				elif grid[nd[1]][nd[0]] == " ":
					pass
				else:
					pos = nd
				
	return (pos[1]+1)*1000 + (pos[0]+1)*4 + facing


p1()
p2()
