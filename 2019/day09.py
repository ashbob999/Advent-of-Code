from typing import Callable
from os.path import isfile, join as path_join

file_name = path_join('input', 'day09.txt')


def to_list(mf: Callable = int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]


def to_gen(mf: Callable = int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)


if not isfile(file_name):
	from aoc import get_input_file

	get_input_file()

from intcode_machine import IntCodeVM

instr = list(map(int, open(file_name).read().strip().split(",")))


def pad_list(arr, amount):
	for i in range(amount):
		arr.append(0)


pad_list(instr, len(instr) * 10)


def part1():
	vm = IntCodeVM(instr[:], [1])
	vm.run()
	return vm.program_outputs[0]


def part2():
	vm = IntCodeVM(instr[:], [2])
	vm.run()
	return vm.program_outputs[0]


print(part1())
print(part2())
