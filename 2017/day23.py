# @formatter:off
from os.path import isfile, join as path_join
from sys import path as sys_path
sys_path.insert(1, path_join(sys_path[0], '..'))
file_name = path_join('input', 'day23.txt')
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
		self.registers = {c: 0 for c in "abcdefgh"}
		self.mul_count = 0

	def run(self):
		while 0 <= self.pc < len(self.instr):
			inst = self.instr[self.pc]

			if inst[0] == "set":
				if is_num(inst[2]):
					value = int(inst[2])
				else:
					value = self.registers[inst[2]]

				self.registers[inst[1]] = value
				self.pc += 1
			elif inst[0] == "sub":
				if is_num(inst[2]):
					value = int(inst[2])
				else:
					value = self.registers[inst[2]]

				self.registers[inst[1]] -= value
				self.pc += 1
			elif inst[0] == "mul":
				if is_num(inst[2]):
					value = int(inst[2])
				else:
					value = self.registers[inst[2]]

				self.registers[inst[1]] *= value
				self.pc += 1
				self.mul_count += 1
			elif inst[0] == "jnz":
				if is_num(inst[1]):
					value = int(inst[1])
				else:
					value = self.registers[inst[1]]

				if is_num(inst[2]):
					offset = int(inst[2])
				else:
					offset = self.registers[inst[2]]

				if value != 0:
					self.pc += offset
				else:
					self.pc += 1


def part1():
	vm = VM(instr)
	vm.run()
	return vm.mul_count


def part2():
	b = int(instr[0][2])
	b *= 100
	b += 100000
	c = b
	c += 17000

	h = 0

	for b in range(b, c + 17, 17):
		f = 1
		for d in range(2, b):
			if b % d == 0:
				if b // d >= 2:
					f = 0
					break

		if f == 0:
			h += 1

	return h


p1()
p2()

"""
set b 57
set c b
jnz a 2
jnz 1 5
mul b 100
sub b -100000
set c b
sub c -17000
set f 1         >3
set d 2
set e 2         >2
set g d         >1
mul g e
sub g b
jnz g 2
set f 0
sub e -1
set g e
sub g b
jnz g -8        <1
sub d -1
set g d
sub g b
jnz g -13       <2
jnz f 2
sub h -1
set g b
sub g c
jnz g 2
jnz 1 3
sub b -17
jnz 1 -23       <3

loops
func 1 {
	# f=1, e=2, d=constant
	# b is multiple of 17
	do {
		# happens b - 1 times
		# e: 2 -> b-1
	
		g = d
		g *= e # g = d*e = d*e
		g -= b # 
		
		if g == 0 { # d*e == b
			f = 0
		}
		
		e += 1
		g = e
		g -= b # g=e-b
		
		# if e == b then return
		
	} while g != 0
}

func 2 {
	# f=1, d=2
	# b is multiple of 17
	do {
		# happens b - 1 times
		# d: 2 -> b-1
		
		e = 2
		func 1() # may set f = 0
		d += 1
		g = d
		g -= b # g=d-b
		
		# if d == b then return
	} while g != 0
}

func 3 {
	do {
		# part 1: b=57, c=57
		# so only happens once
		
		# part 2: b=105700, c=122700
		# so happens c-b // 17 = 1001 times
	
		f = 1
		d = 2
		func 2()
		
		if f == 0 {
			h += 1
		}
		
		# g = b - c
		g = b
		g -= c
		
		# b - c == 0 -> b == c
		if g == 0 {
			end
		}
		
		b += 17
	} while true
}

main {
	# part 1: a = 0
	# part 2: a = 1
	b = 57
	c = b # c = 57
	
	if a != 0 {
		b *= 100 # b = 5700
		b += 100000 # b = 105700
		c = b # c = 105700
		c += 17000 # c = 122700
		# 
	}
	
	func 3()
}

which becomes
h = 0
for b in range(b, c + 17, 17):
	f = 1
	for d in range(2, b):
		for e in range(2, b):
			if d*e == b:
				f = 0
				break
		
		if f == 0:
			break

	if f == 0:
		h += 1
		
and simplifies to
h = 0
for b in range(b, c + 17, 17):
	f = 1
	for d in range(2, b):
		if b % d == 0:
			if b // d >= 2:
				f = 0
				break

	if f == 0:
		h += 1
"""
