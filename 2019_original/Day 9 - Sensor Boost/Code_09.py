from aoc import input_handler
from aoc.aoc.util import intcode_machine

lines = input_handler.get_input(9)

# lines[0] = "109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99"

instr = list(map(int, lines[0].split(",")))


def pad_list(arr, amount):
	for i in range(amount):
        arr.append(0)


# part 1
# print(instr)
pad_list(instr, len(instr) * 10)
# print(instr)
input_value = 1

vm = intcode_machine.IntCodeVM(instr, [input_value])
vm.run()

print("Part 1: ", vm.program_outputs)

# part 2
input_value = 2

vm = intcode_machine.IntCodeVM(instr, [input_value])
vm.run()

print("Part 2: ", vm.program_outputs)
