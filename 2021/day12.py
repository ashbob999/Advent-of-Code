from os.path import isfile, join as path_join
from sys import path as sys_path
sys_path.insert(1, path_join(sys_path[0], '..'))
file_name = path_join('input', 'day12.txt')
def to_list(mf: object = int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]
def to_gen(mf: object = int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)
def p1(*args): ans = part1(*args); print(ans); return ans
def p2(*args): ans = part2(*args); print(ans); return ans

if not isfile(file_name):
	from aoc import get_input_file
	get_input_file(session_path=['..', '.env'])

from utils import parsefile, parse

data = parsefile(file_name, [[str, "-"], "\n"])

graph = {}

for d in data:
	if d[0] in graph:
		graph[d[0]].add(d[1])
	else:
		graph[d[0]] = set([d[1]])
		
	if d[1] in graph:
		graph[d[1]].add(d[0])
	else:
		graph[d[1]] = set([d[0]])


def find_paths(paths, curr_path):
	if curr_path[-1] == "end":
		paths.add(tuple(curr_path))
		return
		
	last = curr_path[-1]
	
	for node in graph[last]:
		if node == "start":
			continue
		
		if node == "end":
			find_paths(paths, curr_path + [node])
		else:
			if "a" <= node[0] <= "z":
				if node not in curr_path:
					find_paths(paths, curr_path + [node])
			else:
				find_paths(paths, curr_path + [node])
		
	return

def part1():
	paths = set()
	find_paths(paths, ["start"])
	return len(paths)

def find_paths2(paths, curr_path, has_2=False):
	if curr_path[-1] == "end":
		paths.add(tuple(curr_path))
		return
		
	last = curr_path[-1]
	
	for node in graph[last]:
		if node == "start":
			continue
		
		if node == "end":
			find_paths2(paths, curr_path + [node], has_2)
		else:
			if "a" <= node[0] <= "z":
				if node not in curr_path:
					find_paths2(paths, curr_path + [node], has_2)
				elif not has_2:
					find_paths2(paths, curr_path + [node], True)
			else:
				find_paths2(paths, curr_path + [node], has_2)
		
	return

def part2():
	paths = set()
	find_paths2(paths, ["start"])
	return len(paths)


p1()
p2()
