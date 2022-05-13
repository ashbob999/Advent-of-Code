# @formatter:off
from os.path import isfile, join as path_join
from sys import path as sys_path
sys_path.insert(1, path_join(sys_path[0], '..'))
file_name = path_join('input', 'day15.txt')
def to_list(mf: object = int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]
def to_gen(mf: object = int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)
def p1(*args): ans = part1(*args); print(ans); return ans
def p2(*args): ans = part2(*args); print(ans); return ans

if not isfile(file_name):
	from aoc import get_input_file
	get_input_file()
# @formatter:on

from utils import parsefile

data = parsefile(file_name, [[" "], "\n"])

discs = []
for d in data:
	id = int(d[1][1:])
	positions = int(d[3])
	time = int(d[6].split("=")[1].split(",")[0])
	position = int(d[11][:-1])

	discs.append([id, time, position, positions])


def part1():
	t = 0
	while True:
		if all((t + i + 1 + disc[2]) % disc[3] == 0 for i, disc in enumerate(discs)):
			break

		t += 1

	return t


def part2():
	discs.append([len(discs) + 1, 0, 0, 11])

	t = 0
	while True:
		if all((t + i + 1 + disc[2]) % disc[3] == 0 for i, disc in enumerate(discs)):
			break

		t += 1

	return t


p1()
p2()
