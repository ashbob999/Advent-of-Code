from typing import Callable
from os.path import isfile, join as path_join

file_name = path_join('input', 'day07.txt')


def to_list(mf: Callable = int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]


def to_gen(mf: Callable = int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)


if not isfile(file_name):
	from aoc import get_input_file

	get_input_file()


class OpType:
	NOT = 0,
	AND = 1,
	OR = 2,
	LSHIFT = 3,
	RSHIFT = 4,
	NUMBER = 5,
	SET = 6


connections = open(file_name).read().strip().split("\n")


def solve(conns, rep=None):
	circuit = {}
	for conn in conns:
		in_signal, out_signal = conn.split("->")
		key = out_signal.strip()

		parts = in_signal.strip().split(" ")

		if len(parts) == 1 and parts[0].isnumeric():
			value = (OpType.NUMBER, int(parts[0]))
		elif len(parts) == 1:
			value = (OpType.SET, parts[0])
		elif parts[0] == "NOT":
			value = (OpType.NOT, parts[1])
		elif parts[1] == "AND":
			value = (OpType.AND, parts[0], parts[2])
		elif parts[1] == "OR":
			value = (OpType.OR, parts[0], parts[2])
		elif parts[1] == "LSHIFT":
			value = (OpType.LSHIFT, parts[0], int(parts[2]))
		elif parts[1] == "RSHIFT":
			value = (OpType.RSHIFT, parts[0], int(parts[2]))

		circuit[key] = value

	done_signals = {}

	for k, v in list(circuit.items()):
		if v[0] == OpType.NUMBER:
			done_signals[k] = v[1]
			circuit.pop(k)

	if rep:
		for k, v in rep.items():
			done_signals[k] = v

	while len(circuit):
		for k, v in list(circuit.items()):
			if v[0] == OpType.SET:
				if v[1] in done_signals:
					done_signals[k] = done_signals[v[1]]
					circuit.pop(k)

			elif v[0] == OpType.NOT or v[0] == OpType.LSHIFT or v[0] == OpType.RSHIFT:
				if v[1] in done_signals:
					val = int(v[1]) if v[1].isnumeric() else done_signals[v[1]]
					if v[0] == OpType.NOT:
						signal = ~val & 0xFFFF
					elif v[0] == OpType.LSHIFT:
						signal = (val << v[2]) & 0xFFFF
					elif v[0] == OpType.RSHIFT:
						signal = val >> v[2]

					done_signals[k] = signal
					circuit.pop(k)

			elif v[0] == OpType.AND or v[0] == OpType.OR:
				if (v[1].isnumeric() or v[1] in done_signals) and (v[2].isnumeric() or v[2] in done_signals):
					val1 = int(v[1]) if v[1].isnumeric() else done_signals[v[1]]
					val2 = int(v[2]) if v[2].isnumeric() else done_signals[v[2]]
					if v[0] == OpType.AND:
						signal = val1 & val2
					elif v[0] == OpType.OR:
						signal = val1 | val2

					done_signals[k] = signal
					circuit.pop(k)

	return done_signals["a"]


def part1():
	return solve(connections)


def part2(a_val):
	return solve(connections, {"b": a_val})


p1 = part1()
print(p1)
print(part2(p1))
