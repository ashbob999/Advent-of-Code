# @formatter:off
from os.path import isfile, join as path_join
from sys import path as sys_path
sys_path.insert(1, path_join(sys_path[0], '..'))
file_name = path_join('input', 'day07.txt')
def to_list(mf: object = int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]
def to_gen(mf: object = int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)
def p1(*args): ans = part1(*args); print(ans); return ans
def p2(*args): ans = part2(*args); print(ans); return ans

if not isfile(file_name):
	from aoc import get_input_file
	get_input_file(session_path=['..', '.env'])
# @formatter:on

from utils import parsefile, Merge

nodes = parsefile(file_name, [[str, 1, str, 1, None, 1, Merge([str, ","]), 0], "\n"])


class Node:
	def __init__(self, name, weight):
		self.name = name
		self.weight = weight
		self.child_nodes = []
		self.parent_node = None

	def calc_weight(self):
		s = self.weight
		for c in self.child_nodes:
			s += c.calc_weight()

		return s

	def is_balanced(self):
		if len(self.child_nodes) == 0:
			return True, 0

		counts = {}
		for c in self.child_nodes:
			res = c.is_balanced()
			if not res[0]:
				return res

			cw = c.calc_weight()
			if cw in counts:
				counts[cw] += 1
			else:
				counts[cw] = 1

		if len(counts) == 1:
			return True, 0

		if len(counts) > 2:
			return False, -1

		sl = sorted(counts.items(), key=lambda x: x[1])
		diff = sl[1][0] - sl[0][0]

		tn = None
		for c in self.child_nodes:
			if c.calc_weight() == sl[0][0]:
				tn = c
				break

		return False, tn.weight + diff


node_dict = {}

for n in nodes:
	w = int(n[1][1:-1])
	node = Node(n[0], w)
	node_dict[n[0]] = node

# build tree
for n in nodes:
	node = node_dict[n[0]]
	for c in n[2:]:
		c_node = node_dict[c]
		node.child_nodes.append(c_node)
		c_node.parent_node = node

tree_node = None


def part1():
	global tree_node
	for n, node in node_dict.items():
		if node.parent_node is None:
			tree_node = node
			return n


def part2():
	res = tree_node.is_balanced()
	return res[1]


p1()
p2()
