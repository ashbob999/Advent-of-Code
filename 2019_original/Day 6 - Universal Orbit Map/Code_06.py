from aoc import input_handler

lines = input_handler.get_input(6)

orbits = [tuple(line.split(")")) for line in lines]


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


# part 1

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

count = 0

for k in nodes:
    current_parent = nodes[k].parent
    if current_parent is None:
        continue

    while current_parent is not None:
        count += 1
        current_parent = current_parent.parent

print("Part 1: ", count)

# part 2

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

print("Part 2: ", node_index_you + node_index_san)
