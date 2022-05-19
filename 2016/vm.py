class VM:
	def __init__(self, prog):
		self.prog = prog
		self.pc = 0
		self.registers = {"a": 0, "b": 0, "c": 0, "d": 0}
		self.instruction_count = len(prog)

	def run(self):
		while self.pc < self.instruction_count:
			op = self.prog[self.pc]

			if op[0] == "cpy":  # copy
				if op[1] in self.registers:
					self.registers[op[2]] = self.registers[op[1]]
				else:
					self.registers[op[2]] = int(op[1])
				self.pc += 1
			elif op[0] == "inc":  # increment
				self.registers[op[1]] += 1
				self.pc += 1
			elif op[0] == "dec":  # decrement
				self.registers[op[1]] -= 1
				self.pc += 1
			elif op[0] == "jnz":  # jump not zero
				if op[1] in self.registers:
					value = self.registers[op[1]]
				else:
					value = int(op[1])
				if value != 0:
					self.pc += int(op[2])
				else:
					self.pc += 1


class VM_v2:
	def __init__(self, prog):
		self.prog = [[op for op in ops] for ops in prog]
		self.pc = 0
		self.registers = {"a": 0, "b": 0, "c": 0, "d": 0}
		self.instruction_count = len(prog)

	def run(self):
		while self.pc < self.instruction_count:
			op = self.prog[self.pc]

			if op[0] == "cpy":  # copy
				if op[2] in self.registers:  # valid
					if op[1] in self.registers:
						self.registers[op[2]] = self.registers[op[1]]
					else:
						self.registers[op[2]] = int(op[1])

				self.pc += 1
			elif op[0] == "inc":  # increment
				if op[1] in self.registers:  # valid
					self.registers[op[1]] += 1

				self.pc += 1
			elif op[0] == "dec":  # decrement
				if op[1] in self.registers:  # valid
					self.registers[op[1]] -= 1

				self.pc += 1
			elif op[0] == "jnz":  # jump not zero
				if op[1] in self.registers:
					value = self.registers[op[1]]
				else:
					value = int(op[1])
				if value != 0:
					if op[2] in self.registers:
						index = self.registers[op[2]]
					else:
						index = int(op[2])
					self.pc += index
				else:
					self.pc += 1
			elif op[0] == "tgl":
				if op[1] in self.registers:
					index = self.registers[op[1]]
				else:
					index = int(op[1])

				if 0 <= self.pc + index < self.instruction_count:  # valid
					target = self.prog[self.pc + index]
					if len(target) == 2:
						if target[0] == "inc":
							target[0] = "dec"
						else:
							target[0] = "inc"
					elif len(target) == 3:
						if target[0] == "jnz":
							target[0] = "cpy"
						else:
							target[0] = "jnz"

				self.pc += 1


class VM_v3:
	def __init__(self, prog):
		self.prog = [[op for op in ops] for ops in prog]
		self.pc = 0
		self.registers = {"a": 0, "b": 0, "c": 0, "d": 0}
		self.instruction_count = len(prog)

	def run(self):
		while self.pc < self.instruction_count:
			op = self.prog[self.pc]

			if op[0] == "cpy":  # copy
				if op[2] in self.registers:  # valid
					if op[1] in self.registers:
						self.registers[op[2]] = self.registers[op[1]]
					else:
						self.registers[op[2]] = int(op[1])

				self.pc += 1
			elif op[0] == "inc":  # increment
				if op[1] in self.registers:  # valid
					self.registers[op[1]] += 1

				self.pc += 1
			elif op[0] == "dec":  # decrement
				if op[1] in self.registers:  # valid
					self.registers[op[1]] -= 1

				self.pc += 1
			elif op[0] == "jnz":  # jump not zero
				if op[1] in self.registers:
					value = self.registers[op[1]]
				else:
					value = int(op[1])
				if value != 0:
					if op[2] in self.registers:
						index = self.registers[op[2]]
					else:
						index = int(op[2])
					self.pc += index
				else:
					self.pc += 1
			elif op[0] == "tgl":
				if op[1] in self.registers:
					index = self.registers[op[1]]
				else:
					index = int(op[1])

				if 0 <= self.pc + index < self.instruction_count:  # valid
					target = self.prog[self.pc + index]
					if len(target) == 2:
						if target[0] == "inc":
							target[0] = "dec"
						else:
							target[0] = "inc"
					elif len(target) == 3:
						if target[0] == "jnz":
							target[0] = "cpy"
						else:
							target[0] = "jnz"

				self.pc += 1
			elif op[0] == "mul":  # mul a b c -> a=b*c
				if op[2] in self.registers:
					b = self.registers[op[2]]
				else:
					b = int(op[2])

				if op[3] in self.registers:
					c = self.registers[op[3]]
				else:
					c = int(op[2])

				res = b * c
				self.registers[op[1]] = res

				self.pc += 1
