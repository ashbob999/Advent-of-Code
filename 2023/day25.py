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

#import pydot

#graph = pydot.Dot()
#n = {}

for d in data:
	if d[0] not in nodes:
		nodes[d[0]] = set()
	#if d[0] not in n:
	#	n[d[0]] = pydot.Node(d[0])
	for v in d[1]:
		if v not in nodes:
			nodes[v] = set()
		#if v not in n:
		#	n[v] = pydot.Node(v)
			
		nodes[d[0]].add(v)
		nodes[v].add(d[0])
		
		#edge = pydot.Edge(n[d[0]], n[v])
		#graph.add_edge(edge)


#graph.write_svg("day25_output.svg")

"""
/
/xqh
/nrs

"""

print(len(nodes))

def part1():
	pass


def part2():
	pass


p1()
p2()
