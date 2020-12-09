from typing import Callable
from os.path import isfile, join as path_join
file_name = path_join('input', 'day08.txt')
def to_list(mf: Callable = int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]
def to_gen(mf: Callable = int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)

if not isfile(file_name):
	from aoc import get_input_file
	get_input_file(session_path=['..', '.env'])

data = to_list(mf=str)

from VM import Machine

vm = Machine(data)

def part1():
	vm.run()
	print(vm.acc)


def part2():
	si = ("jmp", "nop")

	vm.swap_items = si
	for i in range(len(data)):
		if data[i][:3] in si and vm.instr[i]:
			# print("in list", i)
			vm.reset()
			vm.swap_index = i
			vm.run()

			if vm.result == 1:
				print(vm.acc)
				return

part1()
part2()
