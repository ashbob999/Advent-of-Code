from typing import Callable
from os.path import isfile, join as path_join

file_name = path_join('input', 'day07.txt')


def to_list(mf: Callable = int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]


def to_gen(mf: Callable = int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)


if not isfile(file_name):
	from aoc import get_input_file

	get_input_file()

import amplifier_circuit

from itertools import permutations

instr = list(map(int, open(file_name).read().strip().split(",")))

cbs1 = permutations([0, 1, 2, 3, 4])


def part1():
	cbs1 = permutations([0, 1, 2, 3, 4])

	max_output = -1
	part_1_phase_setting = []
	for phase_setting in list(cbs1):
		output = 0

		dispatcher_1 = amplifier_circuit.Dispatcher(instr, 5, [1, 4, 0, 3, 2])
		dispatcher_1.start(0)

		if dispatcher_1.get_output()[0] > max_output:
			max_output = dispatcher_1.get_output()[0]
			part_1_phase_setting = phase_setting

	return max_output


def part2():
	cbs2 = permutations([5, 6, 7, 8, 9])

	max_output2 = -1
	part_2_phase_setting = []
	for phase_setting in list(cbs2):
		output = 0

		dispatcher_2 = amplifier_circuit.Dispatcher(instr, 5, [9, 8, 5, 7, 6])
		dispatcher_2.start(0)

		if dispatcher_2.get_output()[-1] > max_output2:
			max_output2 = dispatcher_2.get_output()[-1]
			part_2_phase_setting = phase_setting

	return max_output2


print(part1())
print(part2())
