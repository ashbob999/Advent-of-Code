# @formatter:off
from os.path import isfile, join as path_join
from sys import path as sys_path
sys_path.insert(1, path_join(sys_path[0], '..'))
file_name = path_join('input', 'day16.txt')
def to_list(mf=int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]
def to_gen(mf=int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)
def p1(*args): ans = part1(*args); print(ans); return ans
def p2(*args): ans = part2(*args); print(ans); return ans

if not isfile(file_name):
	from aoc import get_input_file
	get_input_file(session_path=['..', '.env'])
# @formatter:on

from utils import *

data = parsefile(file_name, ["\n"])
raw = """#################
#...#...#...#..E#
#.#.#.#.#.#.#.#.#
#.#.#.#...#...#.#
#.#.#.#.###.#.#.#
#...#.#.#.....#.#
#.#.#.#.#.#####.#
#.#...#.#.#.....#
#.#.#####.#.###.#
#.#.#.......#...#
#.#.###.#####.###
#.#.#...#.....#.#
#.#.#.#####.###.#
#.#.#.........#.#
#.#.#.#########.#
#S#.............#
#################"""
#data = parse(raw, ["\n"])


w = len(data[0])
h = len(data)

dirs = ((0, -1), (1, 0), (0, 1), (-1, 0)) 

import heapq

def get_path(start, dir, score, end, g, scores, seen):
	
	cs = set([start])
	
	to_check = []
	
	s2 = {}
	dm = {}
	for (p, d), s in scores.items():
		if p not in s2 or s2[p] > s:
			s2[p] = s
			dm[p] = d
	
	target = s2[end]
	
	next = []
	if start == end and score == target:
		#print("end", score)
		return cs
	
	curr = start
	
	#print("curr", curr, score)
	#if curr == (15, 8): print("------")
	#if curr == (5, 13): print("------")
	#score = s2[start]
	#score = s
	
	for i, d in enumerate(dirs):
		nx = curr[0] + d[0]
		ny = curr[1] + d[1]
		
		if (nx, ny) in seen:
			#print("skip", nx, ny)
			continue
			
		ns = score + 1
		if dir != i:
			ns += 1000
		#print("ns",nx, ny, ns, target)

		if g[ny][nx] != "#":
			#if ((nx, ny), i) in scores:
			#	print("sc",scores[((nx, ny), i)])
			#print("n", nx, ny, ((nx, ny), d) in scores)
			if ((nx, ny), i) in scores and ns <= target and (ns == scores[((nx, ny), i)] or ns == scores[((nx, ny), i)]-1000):
				next.append(((nx, ny), i, ns))

	#print(curr, next)
	has_path = False
	for n, d, s in next:
		r = get_path(n, d, s, end, g, scores, seen | set([start]))
		if r is not None:
			has_path = True
			cs |= r
	
	if has_path:
		return cs
	else:
		return None


def dfs(start, dir, end, g):
	
	seen = set()
	scores = {}
	scores[(start, dir)] = 0
	
	to_check = []
	heapq.heappush(to_check, (0, start, dir))
	#to_check = [(start, dir)]
	
	es = []
	
	while len(to_check):
		_, curr, dir = heapq.heappop(to_check)
		
		score = scores[(curr, dir)]
		seen.add((curr, dir))
		
		for i, d in enumerate(dirs):
			nx = curr[0] + d[0]
			ny = curr[1] + d[1]
			
			if g[ny][nx] != "#":
				ns = score + 1
				if dir != i:
					ns += 1000
				
				if (nx, ny) == end:
					print("end", ns)
					if len(es) > 0 and ns > es[-1]:
						return es[0], get_path(start, 1,0,end, g, scores, set())
					es.append(ns)
					#if 
					#return score, get_path(start, end, g, scores)
				
				if ((nx, ny), i) not in seen or ns < scores[((nx, ny), i)]:
					heapq.heappush(to_check, (ns, (nx, ny), i))
					scores[((nx, ny), i)] = ns
	#print(len(scores))
	#print(sorted(es))
	return None
	return sorted(es)[0], get_path(start, end, g, scores)
	
s = (1, h-2)
e = (w-2, 1)
assert data[s[1]][s[0]] == "S"
assert data[e[1]][e[0]] == "E"

score, path = dfs(s, 1, e, data)

def part1():
	return score


def part2():
	print(path)
	print()
	
	for y in range(w):
		for x in range(h):
			if (x, y) in path:
				print("O", end="")
			else:
				print(data[y][x], end="")
				
		print()
	print()
	
	return len(set(path))


p1()
p2()
