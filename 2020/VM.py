

class Machine:
	result = {
		0: "Infinte Loop",
		1: "End Of Program"
	}

	def __init__(self, prog, inf=True, swap_index=-1, swap_items=None):
		self.prog = prog
		self.instr = [None] * len(prog)

		self.inf = inf

		self.swap_index = swap_index
		if swap_items and len(swap_items) == 2:
			self.swap_items = swap_items
		else:
			self.swap_items = None
			self.swap_index = -1

		self.pc = 0
		self.acc = 0

		self.running = False
		self.result = None

		self.seen = set()

	def run(self):

		while True:
			self.running = True

			if self.pc == len(self.instr):
				self.result = 1
				self.running = False
				return

			if self.inf:
				if self.pc in self.seen:
					self.result = 0
					self.running = False
					return

				self.seen.add(self.pc)

			if not self.instr[self.pc]:
				s = self.prog[self.pc].split(" ")
				self.instr[self.pc] = (s[0], int(s[1]))

			op, value = self.instr[self.pc]

			if self.swap_index >= 0 and self.pc == self.swap_index:
				if op in self.swap_items:
					if op == self.swap_items[0]:
						op = self.swap_items[1]
					else:
						op = self.swap_items[0]

			if op == "nop":
				self.pc += 1

			elif op == "acc":
				self.acc += value
				self.pc += 1

			elif op == "jmp":
				self.pc += value


	def reset(self):
		self.pc = 0
		self.acc = 0

		self.seen = set()
