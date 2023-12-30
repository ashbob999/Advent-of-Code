# @formatter:off
from os.path import isfile, join as path_join
from sys import path as sys_path
sys_path.insert(1, path_join(sys_path[0], '..'))
file_name = path_join('input', 'day25.txt')
def to_list(mf: object = int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]
def to_gen(mf: object = int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)
def p1(*args): ans = part1(*args); print(ans); return ans
def p2(*args): ans = part2(*args); print(ans); return ans

if not isfile(file_name):
	from aoc import get_input_file
	get_input_file(session_path=['..', '.env'])
# @formatter:on

from utils import *

data = parsefile(file_name, [[str, [str], ":"], "\n"])

nodes = {}

for d in data:
	if d[0] not in nodes:
		nodes[d[0]] = set()
	for v in d[1]:
		if v not in nodes:
			nodes[v] = set()

		nodes[d[0]].add(v)
		nodes[v].add(d[0])


def make_path(graph, start, end, dists):
	path = []

	if end in dists and end in graph and start in dists and start in graph:
		if end == start:
			return [start]

		curr_dist = dists[end]
		adj_nodes = graph[end]
		# find adj with curr_dist-1
		for adj in adj_nodes:
			if adj in dists and dists[adj] == curr_dist - 1:
				p = make_path(graph, start, adj, dists)
				if p is not None:
					return [end] + p

		return path
	else:
		return None


def find_furthest(graph, start):
	seen = set()
	dists = {}

	to_check = [(start, 0)]

	while len(to_check) > 0:
		curr, dist = to_check.pop(0)

		dists[curr] = dist
		seen.add(curr)

		for v in graph[curr]:
			if v not in seen or dists[v] > dist + 1:
				to_check.append((v, dist + 1))

	furthest_node, max_dist = max(dists.items(), key=lambda x: x[1])

	return furthest_node, max_dist, make_path(graph, start, furthest_node, dists)


def bfs(graph, start):
	seen = set()

	to_check = [start]

	while len(to_check) > 0:
		curr = to_check.pop(0)

		seen.add(curr)

		for v in graph[curr]:
			if v not in seen:
				to_check.append(v)

	return len(seen)


from random import choice

node_keys = list(nodes.keys())


def part1():
	"""
	Pick a random node
	find the furthest node from it
	remove all edges in path from graph

	repeat 3 times

	check graph has 2 separate sub graphs

	if not repeat

	"""

	while True:
		graph = {k: v.copy() for k, v in nodes.items()}

		def do_iter():
			# pick random node
			node = choice(node_keys)

			furthest_node = find_furthest(graph, node)
			path = furthest_node[2]

			# remove all edges from graph
			for i in range(len(path) - 1):
				n1 = path[i]
				n2 = path[i + 1]
				graph[n1].remove(n2)
				graph[n2].remove(n1)

		do_iter()
		do_iter()
		do_iter()

		count = bfs(graph, choice(node_keys))
		if count != len(nodes):
			return count * (len(nodes) - count)


def part2():
	pass


p1()
p2()
