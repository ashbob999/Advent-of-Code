# @formatter:off
from os.path import isfile, join as path_join
from sys import path as sys_path
sys_path.insert(1, path_join(sys_path[0], '..'))
file_name = path_join('input', 'day08.txt')
def to_list(mf: object = int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]
def to_gen(mf: object = int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)
def p1(*args): ans = part1(*args); print(ans); return ans
def p2(*args): ans = part2(*args); print(ans); return ans

if not isfile(file_name):
	from aoc import get_input_file
	get_input_file(session_path=['..', '.env'])
# @formatter:on

from utils import parsefile

instr = parsefile(file_name, [[str, 2, int, 1, None, 1, str, 3], "\n"])


def part1():
	regs = {}

	for inst in instr:
		if inst[0] not in regs:
			regs[inst[0]] = 0

		if any(c.isdigit() for c in inst[3]):
			v1 = int(inst[3])
		else:
			if inst[3] in regs:
				v1 = regs[inst[3]]
			else:
				v1 = 0

		v2 = int(inst[5])

		if inst[4] == "==":
			cv = v1 == v2
		elif inst[4] == "!=":
			cv = v1 != v2
		elif inst[4] == "<=":
			cv = v1 <= v2
		elif inst[4] == ">=":
			cv = v1 >= v2
		elif inst[4] == "<":
			cv = v1 < v2
		elif inst[4] == ">":
			cv = v1 > v2

		if cv:
			if inst[1] == "inc":
				regs[inst[0]] += inst[2]
			else:
				regs[inst[0]] -= inst[2]

	return max(regs.values())


def part2():
	regs = {}
	max_value = 0

	for inst in instr:
		if inst[0] not in regs:
			regs[inst[0]] = 0

		if any(c.isdigit() for c in inst[3]):
			v1 = int(inst[3])
		else:
			if inst[3] in regs:
				v1 = regs[inst[3]]
			else:
				v1 = 0

		v2 = int(inst[5])

		if inst[4] == "==":
			cv = v1 == v2
		elif inst[4] == "!=":
			cv = v1 != v2
		elif inst[4] == "<=":
			cv = v1 <= v2
		elif inst[4] == ">=":
			cv = v1 >= v2
		elif inst[4] == "<":
			cv = v1 < v2
		elif inst[4] == ">":
			cv = v1 > v2

		if cv:
			if inst[1] == "inc":
				regs[inst[0]] += inst[2]
			else:
				regs[inst[0]] -= inst[2]

			if regs[inst[0]] > max_value:
				max_value = regs[inst[0]]

	return max_value


p1()
p2()
