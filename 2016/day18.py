# @formatter:off
from os.path import isfile, join as path_join
from sys import path as sys_path
sys_path.insert(1, path_join(sys_path[0], '..'))
file_name = path_join('input', 'day18.txt')
def to_list(mf: object = int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]
def to_gen(mf: object = int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)
def p1(*args): ans = part1(*args); print(ans); return ans
def p2(*args): ans = part2(*args); print(ans); return ans

if not isfile(file_name):
	from aoc import get_input_file
	get_input_file()
# @formatter:on

from utils import parsefile

row1_traps = parsefile(file_name, [""])


def check(a, b, c):
	if b == 1:
		if a == c:
			return 0  # safe
		else:
			return 1  # trap
	else:  # b==0
		if a == c:
			return 0  # safe
		else:
			return 1  # trap


def gol(start_row, times):
	width = len(start_row)
	rows = [[1 for _ in range(width)] for _ in range(times)]

	# copy first row
	for i in range(width):
		rows[0][i] = 1 if start_row[i] == "^" else 0

	for i in range(1, times):
		for j in range(width):
			safe = 1

			if j == 0:  # first
				safe = check(0, rows[i - 1][j], rows[i - 1][j + 1])
			elif j == width - 1:  # last
				safe = check(rows[i - 1][j - 1], rows[i - 1][j], 0)
			else:  # middle
				safe = check(rows[i - 1][j - 1], rows[i - 1][j], rows[i - 1][j + 1])

			rows[i][j] = safe

	return rows


def part1():
	rows = gol(row1_traps, 40)

	safe = sum(sum(1 for t in r if t == 0) for r in rows)

	return safe


def part2():
	rows = gol(row1_traps, 400000)

	safe = sum(sum(1 for t in r if t == 0) for r in rows)

	return safe


p1()
p2()
