# @formatter:off
from os.path import isfile, join as path_join
from sys import path as sys_path
sys_path.insert(1, path_join(sys_path[0], '..'))
file_name = path_join('input', 'day04.txt')
def to_list(mf=int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]
def to_gen(mf=int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)
def p1(*args): ans = part1(*args); print(ans); return ans
def p2(*args): ans = part2(*args); print(ans); return ans

if not isfile(file_name):
	from aoc import get_input_file
	get_input_file(session_path=['..', '.env'])
# @formatter:on

from utils import *

g = parsefile(file_name,  [str, "\n"])

	
def check(g, word, x, y):
	w = len(g[0])
	h = len(g)
	
	l = len(word)
	
	found = []
	
	if g[y][x] != word[0]:
		return []
	
	# right
	if x+l <= w:
		if all([word[i] == g[y][x+i] for i in range(l)]):
			found.append(((x, y), 0))
		
	# down
	if y+l <= h:
		if all([word[i] == g[y+i][x] for i in range(l)]):
			found.append(((x, y), 1))
		
	# up
	if y - l >= -1:
		if all([word[i] == g[y-i][x] for i in range(l)]):
			found.append(((x, y), 2))
		
	# left
	if x-l >= -1:
		if all([word[i] == g[y][x-i] for i in range(l)]):
			found.append(((x, y), 3))
			
	# top left
	if x-l >= -1 and y-l >= -1:
		if all([word[i] == g[y-i][x-i] for i in range(l)]):
			found.append(((x, y), 4))
			
	# top right
	if x+l <= w and y-l >= -1:
		if all([word[i] == g[y-i][x+i] for i in range(l)]):
			found.append(((x, y), 5))
			
	# bottom left
	if x-l >= -1 and y+l <= h:
		if all([word[i] == g[y+i][x-i] for i in range(l)]):
			found.append(((x, y), 6))
			
	# bottom right
	if x+l <= w and y+l <= h:
		if all([word[i] == g[y+i][x+i] for i in range(l)]):
			found.append(((x,y), 7))
	
	
	return found

def find(word, g):
	found = []
	w = len(g[0])
	h = len(g)
	
	for y in range(h):
		for x in range(w):
			found += check(g, word, x, y)
	
	return found

def part1():
	return len(find("XMAS", g))

def findx(g, x ,y):
	w = len(g[0])
	h = len(g)
	
	if x - 1 < 0 or x+1 >= w or y-1 <0 or y+1>=h:
		return False
		
	if g[y][x] != "A":
		return False
		
	if set([g[y-1][x-1], g[y+1][x+1]]) == set(["M", "S"]):
		if set([g[y-1][x+1], g[y+1][x-1]]) == set(["S", "M"]):
			return True
			
	return False


def part2():
	c = 0
	
	for y in range(len(g)):
		for x in range(len(g[0])):
			if findx(g, x, y):
				c+= 1
				
	return c
	


p1()
p2()
