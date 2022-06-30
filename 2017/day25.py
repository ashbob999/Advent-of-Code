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

from utils import parsefile

parts = parsefile(file_name, [[str, "\n"], "\n\n"])

begin_state = parts[0][0].split(" ")[-1][:-1]
steps = int(parts[0][1].split(" ")[5])

states = {}

for p in parts[1:]:
	id = p[0].split(" ")[-1][:-1]

	zero_cond = []
	zero_cond.append(int(p[2].split(" ")[-1][:-1]))  # write value
	zero_cond.append(1 if p[3].split(" ")[-1][:-1] == "right" else -1)  # move dir
	zero_cond.append(p[4].split(" ")[-1][:-1])  # next state

	one_cond = []
	one_cond.append(int(p[6].split(" ")[-1][:-1]))  # write value
	one_cond.append(1 if p[7].split(" ")[-1][:-1] == "right" else -1)  # move dir
	one_cond.append(p[8].split(" ")[-1][:-1])  # next state

	states[id] = (zero_cond, one_cond)


def part1():
	tape = {}
	pos = 0
	state = begin_state

	for i in range(steps):
		if pos in tape:
			value = tape[pos]
		else:
			value = 0

		cs = states[state]

		# write value
		tape[pos] = cs[value][0]

		# move the pos
		pos += cs[value][1]

		# change the state
		state = cs[value][2]

	c = 0

	for p in tape:
		if tape[p] == 1:
			c += 1

	return c


def part2():
	pass


p1()
p2()
