# @formatter:off
from os.path import isfile, join as path_join
from sys import path as sys_path
sys_path.insert(1, path_join(sys_path[0], '..'))
file_name = path_join('input', 'day13.txt')
def to_list(mf: object = int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]
def to_gen(mf: object = int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)
def p1(*args): ans = part1(*args); print(ans); return ans
def p2(*args): ans = part2(*args); print(ans); return ans

if not isfile(file_name):
	from aoc import get_input_file
	get_input_file(session_path=['..', '.env'])
# @formatter:on

from utils import parsefile

raw_layers = parsefile(file_name, [[int, ": "], "\n"])

layers = {}
for l in raw_layers:
	layers[l[0]] = l[1]

max_layers = max(layers.keys()) + 1


def move(start_time=0):
	hit = []
	pos = -1
	time = start_time

	for i in range(max_layers):
		# move packet
		pos += 1
		if pos in layers:
			if time % (2 * layers[pos] - 2) == 0:
				hit.append(pos)

		# move scanner
		time += 1

	return hit


def check_hit(start_time=0):
	pos = -1
	time = start_time

	for i in range(max_layers):
		# move packet
		pos += 1
		if pos in layers:
			if time % (2 * layers[pos] - 2) == 0:
				return False

		# move scanner
		time += 1

	return True


def part1():
	hit = move()

	score = 0
	for h in hit:
		score += h * layers[h]

	return score


def part2():
	i = 0
	while True:
		if check_hit(i):
			return i
		i += 1


p1()
p2()
