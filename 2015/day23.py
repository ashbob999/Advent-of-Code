from typing import Callable
from os.path import isfile, join as path_join

file_name = path_join('input', 'day23.txt')


def to_list(mf: Callable = int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]


def to_gen(mf: Callable = int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)


if not isfile(file_name):
	from aoc import get_input_file

	get_input_file()

from enum import IntEnum


class OpType(IntEnum):
	hlf = 0,
	tpl = 1,
	inc = 2,
	jmp = 3,
	jie = 4,
	jio = 5


class VM:
	reg_index = {"a": 0, "b": 1}

	def __init__(self, instructions):
		self.instructions = [tuple()] * len(instructions)
		self.reg = [0, 0]
		self.pc = 0

		for i, instr in enumerate(instructions):
			parts = instr.split()
			if parts[0] == "hlf":
				op = (OpType.hlf, VM.reg_index[parts[1]])
			elif parts[0] == "tpl":
				op = (OpType.tpl, VM.reg_index[parts[1]])
			elif parts[0] == "inc":
				op = (OpType.inc, VM.reg_index[parts[1]])
			elif parts[0] == "jmp":
				op = (OpType.jmp, int(parts[1]))
			elif parts[0] == "jie":
				op = (OpType.jie, VM.reg_index[parts[1][:-1]], int(parts[2]))
			elif parts[0] == "jio":
				op = (OpType.jio, VM.reg_index[parts[1][:-1]], int(parts[2]))

			self.instructions[i] = op

	def run(self):
		while self.pc < len(self.instructions):
			instr = self.instructions[self.pc]

			op = instr[0]
			operands = instr[1:]

			if op == OpType.hlf:
				self.reg[operands[0]] //= 2
				self.pc += 1
			elif op == OpType.tpl:
				self.reg[operands[0]] *= 3
				self.pc += 1
			elif op == OpType.inc:
				self.reg[operands[0]] += 1
				self.pc += 1
			elif op == OpType.jmp:
				self.pc += operands[0]
			elif op == OpType.jie:
				if self.reg[operands[0]] % 2 == 0:
					self.pc += operands[1]
				else:
					self.pc += 1
			elif op == OpType.jio:
				if self.reg[operands[0]] == 1:
					self.pc += operands[1]
				else:
					self.pc += 1


instr = open(file_name).read().strip().split("\n")


def part1():
	vm = VM(instr)
	vm.run()
	return vm.reg[VM.reg_index["b"]]


def part2():
	vm = VM(instr)
	vm.reg[VM.reg_index["a"]] = 1
	vm.run()
	return vm.reg[VM.reg_index["b"]]


print(part1())
print(part2())
