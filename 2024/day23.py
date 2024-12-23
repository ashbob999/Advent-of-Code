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

conns = parsefile(file_name,  [["-"], "\n"])

raw = """kh-tc
qp-kh
de-cg
ka-co
yn-aq
qp-ub
cg-tb
vc-aq
tb-ka
wh-tc
yn-cg
kh-ub
ta-co
de-co
tc-td
tb-wq
wh-td
ta-ka
td-qp
aq-cg
wq-ub
ub-vc
de-ta
wq-aq
wq-vc
wh-yn
ka-de
kh-ta
co-tc
wh-qp
tb-vc
td-yn"""
conns = parse(raw, [["-"], "\n"])


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

def get_size(g):
	#print()
	#print(g)
	for i in range(len(g), 0, -1):
		target = 2 * (i-1)
		#print(i, target)
		
		f = list(filter(lambda x:x[1] >= target, g.items()))
		#print(len(f), f)
		if len(f) >= i:
			return i
	return 0


def part2():
	gs = set()
	
	
	for k, v in graph.items():
		g = {}
		#g[k] = 1
		
		for _ in v:
			g[_] = 1
			
		seen = set()
		to_check = list(v)
		
		while len(to_check):
			k2 = to_check[0]
			to_check.pop(0)
			
			#g[k2] += 1
			
			for v2 in graph[k2]:
				if v2 not in g:
					g[v2] = 1
				else:
					g[v2] += 1
					
				if v2 not in seen:
					seen.add(v2)
					to_check.append(v2)
		
		for _1, _2 in sorted([[v, k] for k, v in g.items()]):
			print(_2, _1)
		print(g)
		s = get_size(g)
		print(s)
		print()


p1()
p2()
