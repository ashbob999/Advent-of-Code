# @formatter:off
from os.path import isfile, join as path_join
from sys import path as sys_path
sys_path.insert(1, path_join(sys_path[0], '..'))
file_name = path_join('input', 'day17.txt')
def to_list(mf: object = int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]
def to_gen(mf: object = int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)
def p1(*args): ans = part1(*args); print(ans); return ans
def p2(*args): ans = part2(*args); print(ans); return ans

if not isfile(file_name):
	from aoc import get_input_file
	get_input_file()
# @formatter:on

from utils import parsefile

passcode = parsefile(file_name, None)

start = (0, 0)
end = (3, 3)

from hashlib import md5


def check(code, path):
	txt = code + path
	res = md5(txt.encode())
	hash = res.hexdigest()

	dirs = [True, True, True, True]  # [up, down, left, right]

	for i in range(4):
		if "0" <= hash[i] <= "9" or hash[i] == "a":
			dirs[i] = False

	return dirs


paths = set()


def solve(code, path, curr_pos):
	dirs = check(code, path)

	next_places = []

	if curr_pos[1] > 0 and dirs[0]:  # up
		next_places.append([(curr_pos[0], curr_pos[1] - 1), path + "U"])

	if curr_pos[1] < 3 and dirs[1]:  # down
		next_places.append([(curr_pos[0], curr_pos[1] + 1), path + "D"])

	if curr_pos[0] > 0 and dirs[2]:  # left
		next_places.append([(curr_pos[0] - 1, curr_pos[1]), path + "L"])

	if curr_pos[0] < 3 and dirs[3]:  # right
		next_places.append([(curr_pos[0] + 1, curr_pos[1]), path + "R"])

	for n in next_places:
		if n[0][0] == end[0] and n[0][1] == end[1]:
			paths.add(n[1])
		else:
			solve(code, n[1], n[0])


def part1():
	solve(passcode, "", start)

	s = sorted(list(paths), key=len)[0]

	return s


def part2():
	solve(passcode, "", start)

	s = sorted(list(paths), key=len, reverse=True)[0]

	return len(s)


p1()
p2()
