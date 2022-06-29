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

from utils import parsefile

raw_moves = parsefile(file_name, [str, ","])

moves = []
for m in raw_moves:
	if m[0] == "s":  # spin
		moves.append([0, int(m[1:])])
	elif m[0] == "x":  # exchange
		split = m[1:].split("/")
		moves.append([1, int(split[0]), int(split[1])])
	elif m[0] == "p":  # partner
		moves.append([2, ord(m[1]) - 97, ord(m[3]) - 97])

start_order = "abcdefghijklmnop"

from collections import deque


def dance(programs, moves):
	for m in moves:
		if m[0] == 0:  # spin
			programs.rotate(m[1])
		elif m[0] == 1:  # exchange
			temp = programs[m[1]]
			programs[m[1]] = programs[m[2]]
			programs[m[2]] = temp
		elif m[0] == 2:  # partner
			i1 = programs.index(m[1])
			i2 = programs.index(m[2])

			temp = programs[i1]
			programs[i1] = programs[i2]
			programs[i2] = temp


def part1():
	programs = deque([ord(c) - 97 for c in start_order])

	dance(programs, moves)

	return "".join([chr(v + 97) for v in programs])


def part2():
	programs = deque([ord(c) - 97 for c in start_order])

	reset_i = 1

	for i in range(1_000_000_000):
		dance(programs, moves)
		s = "".join([chr(v + 97) for v in programs])
		if s == start_order:
			reset_i = i + 1
			break

	steps_after_start = 1_000_000_000 % reset_i

	for i in range(steps_after_start):
		dance(programs, moves)

	return "".join([chr(v + 97) for v in programs])


p1()
p2()
