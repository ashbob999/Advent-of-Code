from collections import deque, MutableMapping


class Memory(MutableMapping):

	def __init__(self, init_vals):
		self.contents = {i: val for i, val in enumerate(init_vals)}

	def __getitem__(self, item):
		if not isinstance(item, int):
			raise TypeError('Index must be an integer')
		try:
			result = self.contents[item]
		except KeyError:
			if item < 0:
				raise
			result = 0
		return result

	def __iter__(self):
		return self.contents.__iter__()

	def __len__(self):
		return max(self.contents.keys())

	def __setitem__(self, key, value):
		self.contents[key] = value

	def __delitem__(self, key):
		del self.contents[key]


class Computer:

	def __init__(self, program):
		self.program = Memory(program)
		self.pointer = 0
		self.relative_base = 0
		self.inputs = deque()

	def set_input(self, value):
		for val in value:
			self.inputs.append(val)

	def run_program(self):
		while self.program[self.pointer] != 99:
			op_code = self.program[self.pointer] % 100
			if op_code == 1:
				self.add()
				yield None
			elif op_code == 2:
				self.multiply()
				yield None
			elif op_code == 3:
				self.read_input()
				yield None
			elif op_code == 4:
				param_1 = self.prepare_get_param(1)
				yield param_1
				self.pointer = self.pointer + 2
			elif op_code == 5:
				self.jump_if_true()
				yield None
			elif op_code == 6:
				self.jump_if_false()
				yield None
			elif op_code == 7:
				self.compare_less_than()
				yield None
			elif op_code == 8:
				self.compare_equal()
				yield None
			elif op_code == 9:
				self.change_relative_base()
				yield None
			else:
				raise ValueError('No such operation ' + str(op_code))
		return

	def change_relative_base(self):
		param = self.prepare_get_param(1)
		self.relative_base = self.relative_base + param
		self.pointer = self.pointer + 2

	def compare_equal(self):
		param_1 = self.prepare_get_param(1)
		param_2 = self.prepare_get_param(2)
		self.set_param(3, int(param_1 == param_2))
		self.pointer = self.pointer + 4

	def compare_less_than(self):
		param_1 = self.prepare_get_param(1)
		param_2 = self.prepare_get_param(2)
		self.set_param(3, int(param_1 < param_2))
		self.pointer = self.pointer + 4

	def jump_if_false(self):
		param_1 = self.prepare_get_param(1)
		param_2 = self.prepare_get_param(2)
		if not param_1:
			self.pointer = param_2
		else:
			self.pointer = self.pointer + 3

	def jump_if_true(self):
		param_1 = self.prepare_get_param(1)
		param_2 = self.prepare_get_param(2)
		if param_1:
			self.pointer = param_2
		else:
			self.pointer = self.pointer + 3

	def read_input(self):
		try:
			self.set_param(1, self.inputs.popleft())
		except IndexError:
			self.set_param(1, -1)
		self.pointer = self.pointer + 2

	def multiply(self):
		param_1 = self.prepare_get_param(1)
		param_2 = self.prepare_get_param(2)
		self.set_param(3, param_1 * param_2)
		self.pointer = self.pointer + 4

	def add(self):
		param_1 = self.prepare_get_param(1)
		param_2 = self.prepare_get_param(2)
		self.set_param(3, param_1 + param_2)
		self.pointer = self.pointer + 4

	def prepare_get_param(self, param_num):
		mode = self.get_mode(param_num)
		val = self.program[self.pointer + param_num]
		if mode == 0:
			result = self.program[val]
		elif mode == 1:
			result = val
		elif mode == 2:
			result = self.program[val + self.relative_base]
		else:
			raise ValueError('Unknown mode {}'.format(mode))
		return result

	def get_mode(self, param_num):
		mode = (self.program[self.pointer] //
		        (10 ** (param_num + 1))) % 10
		if mode not in [0, 1, 2]:
			raise ValueError('Unknown mode {} from {}'
			                 .format(mode, self.program[self.pointer]))
		return mode

	def set_param(self, param_num, value):
		mode = self.get_mode(param_num)
		val = self.program[self.pointer + param_num]
		if mode == 0:
			self.program[val] = value
		elif mode == 2:
			self.program[val + self.relative_base] = value
		else:
			raise ValueError('Unknown mode {}'.format(mode))
