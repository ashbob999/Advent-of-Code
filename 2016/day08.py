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
	get_input_file()
# @formatter:on

from utils import parsefile

raw_instr = parsefile(file_name, [[" "], "\n"])

instr = []
for ins in raw_instr:
	if len(ins) == 2:  # rect
		size = ins[1].split("x")
		instr.append([0, int(size[0]), int(size[1])])
	else:  # rotate
		index = int(ins[2].split("=")[1])
		count = int(ins[4])
		if ins[1] == "row":  # row
			instr.append((1, index, count))
		else:  # column
			instr.append((2, index, count))

# 50 wide, 6 tall -> 50 columns, 6 rows
cols = 50
rows = 6
screen_clear = [[0 for i in range(cols)]] * rows


def rect(screen, w, h):
	for y in range(0, h):
		for x in range(0, w):
			screen[y][x] = 1


def rotate_row(screen, index, count):
	new_screen = [r[:] for r in screen]

	for i in range(cols):
		new_index = (i + count) % cols
		new_screen[index][new_index] = screen[index][i]

	return new_screen


def rotate_column(screen, index, count):
	new_screen = [r[:] for r in screen]

	for i in range(rows):
		new_index = (i + count) % rows
		new_screen[new_index][index] = screen[i][index]

	return new_screen


final_screen = []


def part1():
	screen = [r[:] for r in screen_clear]

	for ins in instr:
		if ins[0] == 0:
			rect(screen, ins[1], ins[2])
		elif ins[0] == 1:
			screen = rotate_row(screen, ins[1], ins[2])
		elif ins[0] == 2:
			screen = rotate_column(screen, ins[1], ins[2])

	global final_screen
	final_screen = screen
	lit = sum(sum(r) for r in screen)
	return lit


def part2():
	output = [["#" if v == 1 else " " for v in r] for r in final_screen]

	for r in output:
		print("".join(map(str, r)))


p1()
p2()
