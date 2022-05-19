# @formatter:off
from os.path import isfile, join as path_join
from sys import path as sys_path
sys_path.insert(1, path_join(sys_path[0], '..'))
file_name = path_join('input', 'day21.txt')
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

password = "abcdefgh"

scrambled_password = "fbgdceah"

operations = []
for d in data:
	if d[0] == "swap":
		if d[1] == "position":
			x = int(d[2])
			y = int(d[5])
			operations.append((0, [x, y]))
		else:
			a = d[2]
			b = d[5]
			operations.append((1, [a, b]))
	elif d[0] == "rotate":
		if d[1] == "based":
			letter = d[6]
			operations.append((3, [letter]))
		else:
			steps = int(d[2])
			dir = -1 if d[1] == "left" else 1
			operations.append((2, [dir, steps]))
	elif d[0] == "reverse":
		x = int(d[2])
		y = int(d[4])
		operations.append((4, [x, y]))
	elif d[0] == "move":
		x = int(d[2])
		y = int(d[5])
		operations.append((5, [x, y]))


def swap_index(arr, x, y):
	tmp = arr[y]
	arr[y] = arr[x]
	arr[x] = tmp


def swap_letter(arr, a, b):
	x = arr.index(a)
	y = arr.index(b)
	swap_index(arr, x, y)


def rotate_steps(arr, dir, steps):
	length = len(arr)
	new_arr = [None] * length
	diff = dir * steps
	for i in range(length):
		# uses negative modulo -1 % 3 == 2 (for c use z = x % y; z += (z < 0) ? y : 0;)
		new_i = (i + diff) % length
		new_arr[new_i] = arr[i]

	for i in range(length):
		arr[i] = new_arr[i]


def rotate_letter(arr, letter):
	steps = arr.index(letter)
	if steps >= 4:
		steps += 1
	steps += 1

	rotate_steps(arr, 1, steps)


def reverse(arr, x, y):
	diff = (y - x + 1) // 2

	for i in range(0, diff):
		swap_index(arr, x + i, y - i)


def move(arr, x, y):
	v = arr.pop(x)
	arr.insert(y, v)


funcs = [swap_index, swap_letter, rotate_steps, rotate_letter, reverse, move]


def scramble(word, ops):
	arr = list(word)

	for op in ops:
		funcs[op[0]](arr, *op[1])

	return "".join(arr)


def part1():
	s = scramble(password, operations)
	return s


def reverse_rotate_steps(arr, dir, steps):
	length = len(arr)
	new_arr = [None] * length
	diff = dir * steps * -1
	for i in range(length):
		# uses negative modulo -1 % 3 == 2 (for c use z = x % y; z += (z < 0) ? y : 0;)
		new_i = (i + diff) % length
		new_arr[new_i] = arr[i]

	for i in range(length):
		arr[i] = new_arr[i]


def reverse_rotate_letter(arr, letter):
	index = arr.index(letter)
	"""
	reverse rotate letter only works for length==8
	start index -> right shifts -> end index
	0 -> 1 -> 1
	1 -> 2 -> 3
	2 -> 3 -> 5
	3 -> 4 -> 7
	4 -> 6 -> 2
	5 -> 7 -> 4
	6 -> 8 -> 6
	7 -> 9 -> 0
	"""
	# mapping[i] = shifts left
	mapping = {1: 1, 3: 2, 5: 3, 7: 4, 2: 6, 4: 7, 6: 8, 0: 9}

	left_shifts = mapping[index]

	rotate_steps(arr, -1, left_shifts)


def reverse_move(arr, x, y):
	v = arr.pop(y)
	arr.insert(x, v)


reverse_funcs = [swap_index, swap_letter, reverse_rotate_steps, reverse_rotate_letter, reverse, reverse_move]


def reverse_scramble(word, ops):
	arr = list(word)

	for i in range(len(ops) - 1, -1, -1):
		op = ops[i]
		reverse_funcs[op[0]](arr, *op[1])

	return "".join(arr)


def part2():
	s = reverse_scramble(scrambled_password, operations)
	return s


p1()
p2()
