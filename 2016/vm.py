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
