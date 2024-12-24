# @formatter:off
from os.path import isfile, join as path_join
from sys import path as sys_path
sys_path.insert(1, path_join(sys_path[0], '..'))
file_name = path_join('input', 'day21.txt')
def to_list(mf=int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]
def to_gen(mf=int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)
def p1(*args): ans = part1(*args); print(ans); return ans
def p2(*args): ans = part2(*args); print(ans); return ans

if not isfile(file_name):
	from aoc import get_input_file
	get_input_file(session_path=['..', '.env'])
# @formatter:on

from utils import *

codes = parsefile(file_name, ["\n"])

"""

+---+---+---+
| 7 | 8 | 9 |
+---+---+---+
| 4 | 5 | 6 |
+---+---+---+
| 1 | 2 | 3 |
+---+---+---+
    | 0 | A |
    +---+---+


    +---+---+
    | ^ | A |
+---+---+---+
| < | v | > |
+---+---+---+

"""

# object = (values: points, invalid_points)
# num_keypad = (
# 	{'7': (0, 0), '8': (1, 0), '9': (2, 0), '4': (0, 1), '5': (1, 1), '6': (2, 1), '1': (0, 2), '2': (1, 2),
# 	 '3': (2, 2),
# 	 '0': (1, 3), 'A': (2, 3)}, [(0, 3)])
# dir_keypad = ({'^': (1, 0), 'A': (2, 0), '<': (0, 1), 'v': (1, 1), '>': (2, 1)}, [(0, 0)])

num_seqs = {
	('0', '1'): ['^<'],
	('0', '2'): ['^'],
	('0', '3'): ['^>', '>^'],
	('0', '4'): ['^^<'],
	('0', '5'): ['^^'],
	('0', '6'): ['^^>'],
	('0', '7'): ['^^^<'],
	('0', '8'): ['^^^'],
	('0', '9'): ['^^^>'],
	('0', 'A'): ['>'],

	('1', '0'): ['>v'],
	('1', '2'): ['>'],
	('1', '3'): ['>>'],
	('1', '4'): ['^'],
	('1', '5'): ['^>', '>^'],
	('1', '6'): ['^>>', '>>^'],
	('1', '7'): ['^^'],
	('1', '8'): ['^^>', '>^^'],
	('1', '9'): ['^^>>', '>>^^'],
	('1', 'A'): ['>>v'],

	('2', '0'): ['v'],
	('2', '1'): ['<'],
	('2', '3'): ['>'],
	('2', '4'): ['<^', '^<'],
	('2', '5'): ['^'],
	('2', '6'): ['^>', '>^'],
	('2', '7'): ['^^<', '<^^'],
	('2', '8'): ['^^'],
	('2', '9'): ['^^>', '>^^'],
	('2', 'A'): ['v>', '>^'],

	('3', '0'): ['<^', 'v<'],
	('3', '1'): ['<<'],
	('3', '2'): ['<'],
	('3', '4'): ['<<^', '^<<'],
	('3', '5'): ['<^', '^<'],
	('3', '6'): ['^'],
	('3', '7'): ['<<^^', '^^<<'],
	('3', '8'): ['<^^', '^^<'],
	('3', '9'): ['^^'],
	('3', 'A'): ['v'],

	('4', '0'): ['>vv'],
	('4', '1'): ['v'],
	('4', '2'): ['v>', '>v'],
	('4', '3'): ['v>>', '>>v'],
	('4', '5'): ['>'],
	('4', '6'): ['>>'],
	('4', '7'): ['^'],
	('4', '8'): ['^>', '>^'],
	('4', '9'): ['^>>', '>>^'],
	('4', 'A'): ['>>vv'],

	('5', '0'): ['vv'],
	('5', '1'): ['<v', 'v<'],
	('5', '2'): ['v'],
	('5', '3'): ['v>', '>v'],
	('5', '4'): ['<'],
	('5', '6'): ['>'],
	('5', '7'): ['<^', '^<'],
	('5', '8'): ['^'],
	('5', '9'): ['^>', '>^'],
	('5', 'A'): ['vv>', '>vv'],

	('6', '0'): ['<vv', 'vv<'],
	('6', '1'): ['<<v', 'v<<'],
	('6', '2'): ['<v', 'v<'],
	('6', '3'): ['v'],
	('6', '4'): ['<<'],
	('6', '5'): ['<'],
	('6', '7'): ['<<^', '^<<'],
	('6', '8'): ['<^', '^<'],
	('6', '9'): ['^'],
	('6', 'A'): ['vv'],

	('7', '0'): ['>vvv'],
	('7', '1'): ['vv'],
	('7', '2'): ['vv>', '>vv'],
	('7', '3'): ['vv>>', '>>vv'],
	('7', '4'): ['v'],
	('7', '5'): ['v>', '>v'],
	('7', '6'): ['v>>', '>>v'],
	('7', '8'): ['>'],
	('7', '9'): ['>>'],
	('7', 'A'): ['>>vvv'],

	('8', '0'): ['vvv'],
	('8', '1'): ['<vv', 'vv<'],
	('8', '2'): ['vv'],
	('8', '3'): ['vv>', '>vv'],
	('8', '4'): ['<v', 'v<'],
	('8', '5'): ['v'],
	('8', '6'): ['v>', '>v'],
	('8', '7'): ['<'],
	('8', '9'): ['>'],
	('8', 'A'): ['vvv>', '>vvv'],

	('9', '0'): ['<vvv', 'vvv<'],
	('9', '1'): ['<<vv', 'vv<<'],
	('9', '2'): ['<vv', 'vv<'],
	('9', '3'): ['vv'],
	('9', '4'): ['<<v', 'v<<', ],
	('9', '5'): ['<v', 'v<'],
	('9', '6'): ['v'],
	('9', '7'): ['<<'],
	('9', '8'): ['<'],
	('9', 'A'): ['vvv'],

	('A', '0'): ['<'],
	('A', '1'): ['^<<'],
	('A', '2'): ['<^', '^<'],
	('A', '3'): ['^'],
	('A', '4'): ['^^<<'],
	('A', '5'): ['<^^', '^^<'],
	('A', '6'): ['^^'],
	('A', '7'): ['^^^<<'],
	('A', '8'): ['<^^^', '^^^<'],
	('A', '9'): ['^^^'],
}

dir_seqs = {
	('^', '<'): ['v<'],
	('^', 'v'): ['v'],
	('^', '>'): ['v>', '>v'],
	('^', 'A'): ['>'],

	('v', '^'): ['^'],
	('v', '<'): ['<'],
	('v', '>'): ['>'],
	('v', 'A'): ['^>', '>^'],

	('<', '^'): ['>^'],
	('<', 'v'): ['>'],
	('<', '>'): ['>>'],
	('<', 'A'): ['>>^'],

	('>', '^'): ['<^', '^<'],
	('>', 'v'): ['<'],
	('>', '<'): ['<<'],
	('>', 'A'): ['^'],

	('A', '^'): ['<'],
	('A', 'v'): ['<v', 'v<'],
	('A', '<'): ['v<<'],
	('A', '>'): ['v'],
}

mem = {}


def get_layer_sequence(target, layer_keypad, start='A'):
	# print(len(mem), target)
	seq = ""

	if (tuple(target), layer_keypad, start) in mem:
		return mem[(tuple(target), layer_keypad, start)]

	keypad_seqs = num_seqs if layer_keypad == 0 else dir_seqs

	for i in range(0, len(target)):
		start = target[i - 1] if i > 0 else 'A'
		t = target[i]

		# print(start, t, target)

		if start == t:
			seq += 'A'
		else:
			next_seq = keypad_seqs[(start, t)][0]
			seq += next_seq + 'A'

	mem[(tuple(target), layer_keypad, start)] = seq

	return seq


def do_seq(target, seq):
	final = None

	assert seq[0] == 0

	for i, sq in enumerate(seq):
		next_target = get_layer_sequence(target, sq)
		target = next_target

	final = target

	min_l = len(final)
	return min_l


def get_dir_cost(target):
	after_num = get_layer_sequence(target, 1)

	v = after_num.split('A')

	if v[-1] == '':
		v.pop(-1)

	v = [_ + 'A' for _ in v]

	costs = {}
	for _ in v:
		if _ not in costs:
			costs[_] = 0
		costs[_] += 1

	return costs


def do_seq2(target, dir_count):
	after_num = get_layer_sequence(target, 0)

	v = after_num.split('A')

	if v[-1] == '':
		v.pop(-1)

	v = [_ + 'A' for _ in v]

	costs = {}
	for _ in v:
		if _ not in costs:
			costs[_] = 0
		costs[_] += 1

	for i in range(dir_count):
		new_costs = {}
		for seq, cost in costs.items():
			nc = get_dir_cost(seq)

			for v, c in nc.items():
				if v not in new_costs:
					new_costs[v] = 0
				new_costs[v] += cost * c

		costs = new_costs

	return sum(len(k) * v for k, v in costs.items())


def part1():
	t = 0
	seq = [0, 1, 1]

	for code in codes:
		# print("code", code)
		length = do_seq(code, seq)
		# length = do_seq2(code, 2)

		v = int(code[:-1])

		t += v * length

	return t


def part2():
	t = 0
	seq = [0] + [1] * 25

	for code in codes:
		# print("code", code)
		# length = do_seq(code, seq)
		length = do_seq2(code, 25)

		v = int(code[:-1])

		t += v * length

	return t


p1()
p2()
