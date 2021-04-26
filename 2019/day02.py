from typing import Callable
from os.path import isfile, join as path_join
file_name = path_join('input', 'day02.txt')
def to_list(mf: Callable = int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]
def to_gen(mf: Callable = int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)

if not isfile(file_name):
	from aoc import get_input_file
	get_input_file()

from intcode_machine import IntCodeVM
# intcode_machine.IntCodeVM

instr = list(map(int, open(file_name).read().strip().split(",")))

#instr = [1,1,1,4,99,5,6,0,99]

def part1():
	m_instr = instr[:]
	m_instr[1] = 12
	m_instr[2] = 2
	vm = IntCodeVM(m_instr, [])
	
	vm.run()

	return vm.instructions[0]


def part2():
	desired_output = 19690720
	correct_noun = 0
	correct_verb = 0
	
	for noun in range(0, 100):
		for verb in range(0, 100):
			current_opcodes = instr[:]
			current_opcodes[1] = noun
			current_opcodes[2] = verb
			vm = IntCodeVM(current_opcodes, [])
			vm.run()
			if vm.instructions[0] == desired_output:
				correct_noun = noun
				correct_verb = verb
				break
				
	return 100 * correct_noun + correct_verb


print(part1())
print(part2())
