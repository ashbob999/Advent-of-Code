# @formatter:off
from os.path import isfile, join as path_join
from sys import path as sys_path
sys_path.insert(1, path_join(sys_path[0], '..'))
file_name = path_join('input', 'day24.txt')
def to_list(mf=int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]
def to_gen(mf=int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)
def p1(*args): ans = part1(*args); print(ans); return ans
def p2(*args): ans = part2(*args); print(ans); return ans

if not isfile(file_name):
	from aoc import get_input_file
	get_input_file(session_path=['..', '.env'])
# @formatter:on

from utils import *

dat1, dat2 = parsefile(file_name,  [[[str, int, ": "], "\n"], [[" "], "\n"], "\n\n"])


inputs = {}
for v, val in dat1:
	inputs[v] = val

import graphviz
graph = graphviz.Digraph()

gates = []
for v1, comb, v2, _, out in dat2:
	c = 0
	if comb == "AND":
		c = 0
	elif comb == "OR":
		c = 1
	elif comb == "XOR":
		c = 2
	
	gates.append((v1, c, v2, out))
	graph.node(out)
	graph.node(out + "_"+ comb)
	graph.edge(v1, out + "_" + comb)
	graph.edge(v2, out + "_" + comb)
	graph.edge(out + "_" + comb, out)
	
graph.render("day24_p1_original", format="pdf")
	


def part1():
	g2 = gates.copy()
	vals = inputs.copy()
	
	while len(g2):
		for g in g2:
			if g[0] in vals and g[2] in vals:
				v1 = vals[g[0]]
				v2 = vals[g[2]]
				val = 0
				if g[1] == 0:
					val = v1 & v2
				elif g[1] == 1:
					val = v1 | v2
				elif g[1] == 2:
					val = v1 ^ v2
					
				vals[g[3]] = val
				g2.remove(g)
				break
				
	output = 0
	for v, val in vals.items():
		if v[0] == "z":
			index = int(v[1:])
			output |= val << index
	print(len(vals))
	return output


def part2():
	swaps = {}

	swaps["jst"] = "z05"
	swaps["z05"] = "jst"

	swaps["mcm"] = "gdf"
	swaps["gdf"] = "mcm"

	swaps["z15"] = "dnt"
	swaps["dnt"] = "z15"

	swaps["z30"] = "gwc"
	swaps["gwc"] = "z30"

	graph2 = graphviz.Digraph()

	for v1, comb, v2, _, out in dat2:
		if out in swaps:
			out = swaps[out]
		
		graph2.node(out)
		graph2.node(out + "_"+ comb)
		graph2.edge(v1, out + "_" + comb)
		graph2.edge(v2, out + "_" + comb)
		graph2.edge(out + "_" + comb, out)

	graph2.render("day24_p2_swapped", format="pdf")
	
	return ",".join(sorted(swaps.keys()))


p1()
p2()
