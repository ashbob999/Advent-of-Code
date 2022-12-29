# @formatter:off
from os.path import isfile, join as path_join
from sys import path as sys_path
sys_path.insert(1, path_join(sys_path[0], '..'))
file_name = path_join('input', 'day19.txt')
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
rd = """Blueprint 1:E ach ore robot costs 4 ore. Each clay robot costs 2 ore. Each obsidian robot costs 3 ore and 14 clay. Each geode robot costs 2 ore and 7 obsidian.
Blueprint 2: Each ore robot costs 2 ore. Each clay robot costs 3 ore. Each obsidian robot costs 3 ore and 8 clay. Each geode robot costs 3 ore and 12 obsidian."""
data = parse(rd, [[str, " "], "\n"])

resources = {
	0: "ore",
	1: "clay",
	2: "obsidian",
	3: "geode"
}

blueprints = []

"""
ore: ore
clay: ore
obsidian: ore + clay
geode: ore + obsidian
"""

for d in data:
	ore = [int(d[6]), 0, 0, 0]
	clay = [int(d[12]), 0, 0, 0]
	obsidian = [int(d[18]), int(d[21]), 0, 0]
	geode = [int(d[27]), 0, int(d[30]), 0]
	
	blueprints.append([ore, clay, obsidian, geode])
	
def rec(bp, robots, amount, time):
	print(robots)
	if time == 0:
		return 0
	
	afford = []
	for j in range(4):
		can = True
		for i in range(4):
			if bp[j][i] > amount[i]:
				can = False
				break
				
		if can:
			can.afford.append(j)
			
	amount = amount.copy()
	for i in range(4):
		amount[i] += robots[i]
	print("afford", afford)
	for r in afford:
		amt = amount.copy()
		for i in range(4):
			amt[i] -= bp[r][i]
		rbs = robots.copy()
		rbs[i] += 1
		res = rec(bp, robots, amt)
		
	
	return amount.copy()
	
start_rb = {0:1, 1:0, 2:0, 3:0}
start_amt = {i:0 for i in range(4)}

def part1():
	s = 0
	for i, b in enumerate(blueprints):
		g = rec(b, start_rb.copy(), start_amt.copy(), 24)
		s += g * (i+1)
		print(i, b, s)
		break
		
	return s


def part2():
	pass


p1()
p2()
