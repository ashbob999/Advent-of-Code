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
	get_input_file()
# @formatter:on

from utils import parsefile

init_state = parsefile(file_name, "")


def step(state):
	# copy state
	new_state = state[:]

	# reverse chars
	new_state = new_state[::-1]

	# swap all 1 and 0's around
	for i in range(len(new_state)):
		if new_state[i] == "0":
			new_state[i] = "1"
		else:
			new_state[i] = "0"

	return state + ["0"] + new_state


def checksum(state):
	check = [""] * (len(state) // 2)

	for i in range(0, len(state), 2):
		if state[i] == state[i + 1]:
			check[i // 2] = "1"
		else:
			check[i // 2] = "0"

	# print(check)

	if len(check) % 2 == 0:
		return checksum(check)

	return check


def randomise(size):
	state = init_state[:]
	while len(state) < size:
		state = step(state)

	check = checksum(state[:size])

	return "".join(check)


def part1():
	return randomise(272)


def part2():
	return randomise(35651584)


p1()
p2()
