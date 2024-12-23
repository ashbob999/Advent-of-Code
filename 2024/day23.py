# @formatter:off
from os.path import isfile, join as path_join
from sys import path as sys_path
sys_path.insert(1, path_join(sys_path[0], '..'))
file_name = path_join('input', 'day23.txt')
def to_list(mf=int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]
def to_gen(mf=int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)
def p1(*args): ans = part1(*args); print(ans); return ans
def p2(*args): ans = part2(*args); print(ans); return ans

if not isfile(file_name):
	from aoc import get_input_file
	get_input_file(session_path=['..', '.env'])
# @formatter:on

from utils import *

conns = parsefile(file_name, [["-"], "\n"])

graph = {}
for c1, c2 in conns:
	if c1 not in graph:
		graph[c1] = set()
	graph[c1].add(c2)

	if c2 not in graph:
		graph[c2] = set()
	graph[c2].add(c1)


def part1():
	c = 0

	gs = set()

	for k, v in graph.items():
		if not k.startswith("t"):
			continue

		for k2 in v:
			v2 = graph[k2]

			for k3 in v2:
				v3 = graph[k3]

				if k in v3 and k2 in v3:
					gs.add(frozenset([k, k2, k3]))

	return len(gs)


seen = set()


def find_groups(cg, latest, groups, lg):
	if (frozenset(cg), latest) in seen:
		return
	seen.add((frozenset(cg), latest))

	if len(lg[0]) < len(cg):
		lg[0] = cg.copy()

	for v in graph[latest]:
		if v in cg:
			continue

		vals = graph[v]

		if all(_ in vals for _ in cg):
			new_cg = cg.copy()
			new_cg.add(v)
			find_groups(new_cg, v, groups, lg)


def part2():
	gs = set()

	lg = [set()]

	for k, v in graph.items():
		find_groups(set(), k, gs, lg)

	value = lg[0]

	return ",".join(sorted(list(value)))


p1()
p2()
