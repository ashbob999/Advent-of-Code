# @formatter:off
from os.path import isfile, join as path_join
from sys import path as sys_path
sys_path.insert(1, path_join(sys_path[0], '..'))
file_name = path_join('input', 'day15.txt')
def to_list(mf=int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]
def to_gen(mf=int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)
def p1(*args): ans = part1(*args); print(ans); return ans
def p2(*args): ans = part2(*args); print(ans); return ans

if not isfile(file_name):
	from aoc import get_input_file
	get_input_file(session_path=['..', '.env'])
# @formatter:on

from utils import *

data, moves = parsefile(file_name,  [["\n"], [str, "\n"], "\n\n"])

all_moves = "".join(moves)

w = len(data[0])
h = len(data)

blocks = set()

start = None

for y in range(h):
	for x in range(w):
		v = data[y][x]
		
		if v == "@":
			start = (x, y)
		elif v == "O":
			blocks.add((x, y))

dirs = {"<": (-1, 0), ">": (1, 0), "^": (0, -1), "v":(0, 1)}

def move(pos, blocks, move):
	dir = dirs[move]
	
	nx = pos[0] + dir[0]
	ny = pos[1] + dir[1]
	
	nv = data[ny][nx]
	if nv == "#":
		return pos, blocks
	elif (nx, ny) not in blocks:
		return (nx, ny), blocks
		
	nb = blocks.copy()
	to_move = []
	
	cx = nx
	cy = ny
	can_move = False
	while data[cy][cx] != "#":
		if (cx, cy) not in blocks:
			can_move = True
			break
			
		to_move.append((cx, cy))
		
		cx += dir[0]
		cy += dir[1]
	
	if not can_move:
		return pos, blocks
	
	for v in to_move[::-1]:
		blocks.remove(v)
		vx = v[0] + dir[0]
		vy = v[1] + dir[1]
		
		blocks.add((vx, vy))
	
	return (nx, ny), blocks
	

def score(b):
	t = 0
	
	for b_ in b:
		t += b_[1] * 100 + b_[0]
	
	return t

def part1():
	b = blocks.copy()
	s = start
	
	for index, m in enumerate(all_moves):
		s, b = move(s, b, m)
	
	t = 0
	
	for b_ in b:
		t += b_[1] * 100 + b_[0]
		
	return t

def in_blocks(p, blocks):
	for b in blocks:
		if b[1] == p[1]:
			if p[0] == b[0] or p[0] == b[0]+1:
				return True
	
	return False

def get_block(p, blocks):
	if p in blocks:
		return p
	
	for b in blocks:
		if p[1] == b[1]:
			if p[0] == b[0] or p[0] == b[0]+1:
				return b
	
	return None


def get_jb(p, dir, blocks, g):
	jb = set()
	
	if not in_blocks(p, blocks):
		return set()
		
	assert dir[0] == 0
	
	b = get_block(p, blocks)
	jb.add(b)
	
	x, y = b
	y += dir[1]
	
	x1 = x
	x2 = x+1
	
	b1 = get_block((x1, y), blocks)
	b2 = get_block((x2, y), blocks)
	
	if b1 == b2:
		if b1 is not None:
			jb |= get_jb(b1, dir, blocks, g)
	else:
		if b1 is not None:
			jb |= get_jb(b1, dir, blocks, g)
		if b2 is not None:
			jb |= get_jb(b2, dir, blocks, g)
		
	
	return jb
	

def move2(pos, blocks, move, g):
	dir = dirs[move]
	
	nx = pos[0] + dir[0]
	ny = pos[1] + dir[1]
	
	nv = g[ny][nx]
	if nv == "#":
		return pos, blocks
	elif not in_blocks((nx, ny), blocks):
		return (nx, ny), blocks
		
	nb = set()
	to_move = set()
	
	cx = nx
	cy = ny
	can_move = False
	
	
	if dir[1] == 0: # hor
		x = nx
		while g[ny][x] != "#":
			if not in_blocks((x, ny), blocks):
				can_move = True
				break
			
			b = get_block((x, ny), blocks)
			to_move.add(b)
				
			x += dir[0]
			
	else: # vert
		jb = get_jb((nx, ny), dir, blocks, g)
		can_move = True
		for b in jb:
			x, y = b
			y += dir[1]
			
			if g[y][x] == "#" or g[y][x+1] == "#":
				can_move = False
				break
				
		to_move = jb
	
	if not can_move:
		return pos, blocks
	
	for v in to_move:
		blocks.remove(v)
		vx = v[0] + dir[0]
		vy = v[1] + dir[1]
		
		nb.add((vx, vy))
		
	for v in blocks:
		nb.add(v)
	
	return (nx, ny), nb


def part2():
	g2 = []
	b2 = set()
	s = None
	
	for y in range(h):
		g2.append("")
		for x in range(w):
			v = data[y][x]
			if v == "#":
				g2[-1] += "##"
			elif v == ".":
				g2[-1] += ".."
			elif v == "@":
				s = (x*2, y)
				g2[-1] += "@."
			elif v == "O":
				g2[-1] += "[]"
				b2.add((x*2, y))
	
	
	for index, m in enumerate(all_moves):
		s, b2 = move2(s, b2, m, g2)
		
	t = 0
	for b_ in b2:
		t += b_[1] * 100 + b_[0]
		
	return t
	

p1()
p2()
