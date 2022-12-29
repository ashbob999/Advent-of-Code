# @formatter:off
from os.path import isfile, join as path_join
from sys import path as sys_path
sys_path.insert(1, path_join(sys_path[0], '..'))
file_name = path_join('input', 'day16.txt')
def to_list(mf: object = int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]
def to_gen(mf: object = int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)
def p1(*args): ans = part1(*args); print(ans); return ans
def p2(*args): ans = part2(*args); print(ans); return ans

if not isfile(file_name):
	from aoc import get_input_file
	get_input_file(session_path=['..', '.env'])
# @formatter:on

from utils import parsefile, parse

data = parsefile(file_name, [[str, " "], "\n"])
rd = """Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
Valve BB has flow rate=13; tunnels lead to valves CC, AA
Valve CC has flow rate=2; tunnels lead to valves DD, BB
Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
Valve EE has flow rate=3; tunnels lead to valves FF, DD
Valve FF has flow rate=0; tunnels lead to valves EE, GG
Valve GG has flow rate=0; tunnels lead to valves FF, HH
Valve HH has flow rate=22; tunnel leads to valve GG
Valve II has flow rate=0; tunnels lead to valves AA, JJ
Valve JJ has flow rate=21; tunnel leads to valve II"""
dataa = parse(rd, [[str, " "], "\n"])

values = []
valves = {}
pos_valves = set()

for line in data:
	id = line[1]
	flow = int(line[4][5:-1])
	tunnels = []
	for i in range(9, len(line)):
		tunnels.append(line[i].replace(",", ""))
		
	values.append((id, flow, tunnels))
	valves[id] = values[-1]
	if flow > 0:
		pos_valves.add(id)

for v in values:
	pass#print(v)

from functools import cache

@cache
def bfs(curr_valve, time_left, valves_open):
	if time_left <= 1:
		return 0
		
	max_flow = 0
	
	for valve in valves[curr_valve][2]:
		flow = bfs(valve, time_left-1, valves_open)
		max_flow = max(max_flow, flow)
		
	if curr_valve not in valves_open and valves[curr_valve][1] > 0:
		vo = tuple(sorted([*valves_open, curr_valve]))
		flow = bfs(curr_valve, time_left -1, vo)
		flow += valves[curr_valve][1] * (time_left - 1)
		max_flow = max(max_flow, flow)
		
	return max_flow
	

def part1():
	return bfs("AA", 30, tuple())


def part2():
	pass


p1()
p2()
