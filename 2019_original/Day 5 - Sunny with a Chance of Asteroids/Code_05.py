# link to Day 1: https://adventofcode.com/2019/day/5

from aoc import input_handler
from aoc.aoc.util import intcode_machine

lines = input_handler.get_input(5)

instructions = list(map(int, lines[0].split(",")))

# Part 1

ic_1 = intcode_machine.IntCodeVM(list(map(int, lines[0].split(","))), [1])

ic_1.run()

print(ic_1.program_outputs)
print("Part 1: ", ic_1.program_outputs[-1])

# Part 2

# print("at 0: ", instructions[0])
print()

ic_2 = intcode_machine.IntCodeVM(list(map(int, lines[0].split(","))), [5])

ic_2.run()

print(ic_2.program_outputs)
print("Part 2: ", ic_2.program_outputs[-1])
