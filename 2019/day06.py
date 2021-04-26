from typing import Callable
from os.path import isfile, join as path_join
file_name = path_join('input', 'day06.txt')
def to_list(mf: Callable = int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]
def to_gen(mf: Callable = int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)

if not isfile(file_name):
	from aoc import get_input_file
	get_input_file()

orbits = map(lambda x: tuple(x.split(")")), open(file_name).read().strip().split("\n"))

# (A, B) -> B orbits A

class Tree:
    def __init__(self, name, parent=None, children=None):
        self.name = name
        self.children = set()
        self.parent = parent

        if children is not None:
            for child in children:
                self.add_child(child)

    def add_child(self, child):
        self.children.add(child)


nodes = {}

for orbit in orbits:
    child_n = orbit[1]
    parent_n = orbit[0]

    if parent_n in nodes:
        parent = nodes[parent_n]
    else:
        parent = Tree(parent_n)
        nodes[parent_n] = parent

    if child_n in nodes:
        child = nodes[child_n]
    else:
        child = Tree(child_n, parent)
        nodes[child_n] = child

    child.parent = parent
    parent.add_child(child)


def part1():
	count = 0

	for k in nodes:
		current_parent = nodes[k].parent
		if current_parent is None:
			continue

		while current_parent is not None:
			count += 1
			current_parent = current_parent.parent
			
	return count


def part2():
	node_you = nodes["YOU"]
	node_san = nodes["SAN"]

	node_you_parents = []
	node_san_parents = []

	tmp_node = node_you.parent

	while tmp_node is not None:
		node_you_parents.append(tmp_node)
		tmp_node = tmp_node.parent

	tmp_node = node_san.parent

	while tmp_node is not None:
		node_san_parents.append(tmp_node)
		tmp_node = tmp_node.parent

	first_shared_node = None
	for i in range(1, min(len(node_you_parents), len(node_san_parents)) + 1, 1):
		if node_you_parents[-i] == node_san_parents[-i]:
			first_shared_node = node_you_parents[-i]

	node_index_you = node_you_parents.index(first_shared_node)
	node_index_san = node_san_parents.index(first_shared_node)

	return node_index_san + node_index_you


print(part1())
print(part2())
