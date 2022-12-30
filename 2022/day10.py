# @formatter:off
from os.path import isfile, join as path_join
from sys import path as sys_path
sys_path.insert(1, path_join(sys_path[0], '..'))
file_name = path_join('input', 'day10.txt')
def to_list(mf: object = int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]
def to_gen(mf: object = int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)
def p1(*args): ans = part1(*args); print(ans); return ans
def p2(*args): ans = part2(*args); print(ans); return ans

if not isfile(file_name):
	from aoc import get_input_file
	get_input_file(session_path=['..', '.env'])
# @formatter:on

from utils import parsefile

instr = parsefile(file_name, [[str, " "], "\n"])

class VM:
	def __init__(self, instr):
		self.prog = [inst[:] for inst in instr]
	
		self.latency = {"addx": 2, "noop": 1}
	
		self.reg = {"x": 1}
		self.pc = 0
		self.cycles = 0
		self.queue = []
		self.signals = []
		self.crt = [[" " for x in range(40)] for y in range(6)]

	def run(self):
		while len(self.queue) > 0 or self.pc < len(self.prog):
			self.cycles += 1
			
			if len(self.queue) ==0 and self.pc < len(self.prog):
				inst = self.prog[self.pc]
				self.queue.append([inst, self.latency[inst[0]]])
				self.pc += 1

			#print(self.queue)
			for inst in self.queue:
				inst[1] -= 1
						
			if self.cycles >= 20:
				if (self.cycles - 20) % 40 == 0:
					self.signals.append(self.cycles * self.reg["x"])
			
			for inst in self.queue:
				if inst[1] == 0:
					op = inst[0]
					if op[0] == "addx":
						self.reg["x"] += int(op[1])
					elif op[0] == "noop":
						pass

			self.queue = [inst for inst in self.queue if inst[1] > 0]
			
			y = self.cycles // 40
			x = self.cycles % 40
			
			sprite = [self.reg["x"]]
			sprite.append(sprite[0]-1)
			sprite.append(sprite[0]+1)
			
			if x in sprite:
				self.crt[y][x] = "#"
			
			

def part1():
	vm = VM(instr)
	vm.run()
	return sum(vm.signals)


def part2():
	vm = VM(instr)
	vm.run()
	return "\n".join(["".join(r) for r in vm.crt])


p1()
p2()
