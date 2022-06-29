# @formatter:off
from os.path import isfile, join as path_join
from sys import path as sys_path
sys_path.insert(1, path_join(sys_path[0], '..'))
file_name = path_join('input', 'day18.txt')
def to_list(mf: object = int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]
def to_gen(mf: object = int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)
def p1(*args): ans = part1(*args); print(ans); return ans
def p2(*args): ans = part2(*args); print(ans); return ans

if not isfile(file_name):
	from aoc import get_input_file
	get_input_file(session_path=['..', '.env'])
# @formatter:on

from utils import parsefile

instr = parsefile(file_name, [[str], "\n"])


def is_num(s: str):
	if s[0] == "-":
		return s[1:].isdigit()
	return s.isdigit()


class VM:
	def __init__(self, instr):
		self.instr = [inst[:] for inst in instr]
		self.pc = 0
		self.registers = {}
		self.played_sounds = []

	def run(self):
		while 0 <= self.pc < len(self.instr):
			inst = self.instr[self.pc]

			if inst[0] == "snd":
				if is_num(inst[1]):
					value = int(inst[1])
				else:
					value = self.registers[inst[1]]

				self.played_sounds.append(value)
				self.pc += 1
			elif inst[0] == "set":
				if is_num(inst[2]):
					value = int(inst[2])
				else:
					value = self.registers[inst[2]]

				self.registers[inst[1]] = value
				self.pc += 1
			elif inst[0] == "add":
				if is_num(inst[2]):
					value = int(inst[2])
				else:
					value = self.registers[inst[2]]

				if inst[1] not in self.registers:
					self.registers[inst[1]] = 0

				self.registers[inst[1]] += value
				self.pc += 1
			elif inst[0] == "mul":
				if is_num(inst[2]):
					value = int(inst[2])
				else:
					value = self.registers[inst[2]]

				if inst[1] not in self.registers:
					self.registers[inst[1]] = 0

				self.registers[inst[1]] *= value
				self.pc += 1
			elif inst[0] == "mod":
				if is_num(inst[2]):
					value = int(inst[2])
				else:
					value = self.registers[inst[2]]

				if inst[1] not in self.registers:
					self.registers[inst[1]] = 0

				self.registers[inst[1]] %= value
				self.pc += 1
			elif inst[0] == "rcv":
				if is_num(inst[1]):
					value = int(inst[1])
				else:
					value = self.registers[inst[1]]

				if value != 0:
					return

				self.pc += 1
			elif inst[0] == "jgz":
				if is_num(inst[1]):
					value = int(inst[1])
				else:
					value = self.registers[inst[1]]

				if is_num(inst[2]):
					offset = int(inst[2])
				else:
					offset = self.registers[inst[2]]

				if value > 0:
					self.pc += offset
				else:
					self.pc += 1


def part1():
	vm = VM(instr)
	vm.run()

	return vm.played_sounds[-1]


class VM2:
	def __init__(self, instr, id, inputs=None):
		if inputs is None:
			inputs = []
		self.instr = [inst[:] for inst in instr]
		self.pc = 0
		self.registers = {"p": id}
		self.finished = False
		self.waiting_for_input = False

		if inputs is not None:
			self.inputs = inputs[:]
		else:
			self.inputs = []

		self.outputs = []
		self.send_count = 0
		self.id = id

	def run(self):
		while 0 <= self.pc < len(self.instr):
			inst = self.instr[self.pc]

			if inst[0] == "snd":
				if is_num(inst[1]):
					value = int(inst[1])
				else:
					value = self.registers[inst[1]]

				self.outputs.append(value)
				self.send_count += 1
				self.pc += 1
			elif inst[0] == "set":
				if is_num(inst[2]):
					value = int(inst[2])
				else:
					value = self.registers[inst[2]]

				self.registers[inst[1]] = value
				self.pc += 1
			elif inst[0] == "add":
				if is_num(inst[2]):
					value = int(inst[2])
				else:
					value = self.registers[inst[2]]

				if inst[1] not in self.registers:
					self.registers[inst[1]] = 0

				self.registers[inst[1]] += value
				self.pc += 1
			elif inst[0] == "mul":
				if is_num(inst[2]):
					value = int(inst[2])
				else:
					value = self.registers[inst[2]]

				if inst[1] not in self.registers:
					self.registers[inst[1]] = 0

				self.registers[inst[1]] *= value
				self.pc += 1
			elif inst[0] == "mod":
				if is_num(inst[2]):
					value = int(inst[2])
				else:
					value = self.registers[inst[2]]

				if inst[1] not in self.registers:
					self.registers[inst[1]] = 0

				self.registers[inst[1]] %= value
				self.pc += 1
			elif inst[0] == "rcv":
				if len(self.inputs) != 0:
					self.registers[inst[1]] = self.inputs[0]
					self.inputs.pop(0)
				else:
					return

				self.pc += 1
			elif inst[0] == "jgz":
				if is_num(inst[1]):
					value = int(inst[1])
				else:
					value = self.registers[inst[1]]

				if is_num(inst[2]):
					offset = int(inst[2])
				else:
					offset = self.registers[inst[2]]

				if value > 0:
					self.pc += offset
				else:
					self.pc += 1

		self.finished = True

	def add_inputs(self, inputs):
		self.inputs.extend(inputs)
		if not self.finished:
			self.run()


def part2():
	vm0 = VM2(instr, 0)
	vm1 = VM2(instr, 1)

	while not vm0.finished or not vm1.finished:
		vm0.run()
		vm1.run()

		if len(vm0.outputs) == 0 and len(vm1.outputs) == 0:
			break

		vm0_out = vm0.outputs[:]
		vm0.outputs = []

		vm1_out = vm1.outputs[:]
		vm1.outputs = []

		vm0.add_inputs(vm1_out)
		vm1.add_inputs(vm0_out)

	return vm1.send_count


p1()
p2()
