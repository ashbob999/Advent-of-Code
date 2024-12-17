# @formatter:off
from os.path import isfile, join as path_join
from sys import path as sys_path
sys_path.insert(1, path_join(sys_path[0], '..'))
file_name = path_join('input', 'day17.txt')
def to_list(mf=int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]
def to_gen(mf=int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)
def p1(*args): ans = part1(*args); print(ans); return ans
def p2(*args): ans = part2(*args); print(ans); return ans

if not isfile(file_name):
	from aoc import get_input_file
	get_input_file(session_path=['..', '.env'])
# @formatter:on

from utils import *


data = parsefile(file_name,  [["\n"], 0, str, 1, "\n\n"])
raw = """Register A: 2024
Register B: 0
Register C: 0

Program: 0,3,5,4,3,0"""
#data = parse(raw,  [["\n"], 0, str, 1, "\n\n"])


regs = []
code = []

for r in data[0]:
	v = int(r.split(": ")[1])
	regs.append(v)

code = [int(v) for v in data[1][0].split(": ")[1].split(",")]

print(regs)
print(code)

def run(regs, code):
	
	out = []
	
	def combo(v):
		assert v < 7
		if v <= 3:
			return v
		return regs[v - 4]
	
	pc = 0
	while pc < len(code):
		#print(pc, len(code))
		c = code[pc]
		v = code[pc+1]
		
		if c == 0: # div a - >
			regs[0] = regs[0] // 2**combo(v)
		if c == 1: # xor b literal
			regs[1] = regs[1] ^ v
		if c == 2: # mod 8 b
			regs[1] = combo(v) % 8
		if c == 3: # jnz a
			if regs[0] != 0:
				pc = v
				continue
		if c == 4: # xor b c
			regs[1] = regs[1] ^ regs[2]
		if c == 5: # out mod 8
			out.append(combo(v) % 8)
		if c == 6: # div a -> b
			regs[1] = regs[0] // 2**combo(v)
		if c == 7: # div a -> c
			regs[2] = regs[0] // 2**combo(v)
		
		pc += 2
		
	return regs, out


def part1():
	r, o = run(regs, code)
	
	return ",".join([str(v) for v in o])


"""

2,4, b = a % 8
1,2, b = b ^ 2
7,5, c = a // 2**b -> c = a >> b
4,7, b = b ^ c
1,3, b = b ^ 3
5,5, out b
0,3, a = a // 2**3 -> a = a >> 3
3,0, jnz a -> 0


0 ^ 2 = 2
1 ^ 2 = 3
2 ^ 2 = 0

a, b, c

while a != 0:
	b = a % 8
	
	b ^= 2
	c = a // 2**b (2, 3, 1)
	b = b ^ c
	b = b ^ 3
	
	out b
	
	a >>= 3

"""

def calc(v):
	a, b, c = 0,0,0
	a = v
	
	b = a % 8
	b ^= 2
	c = a // (2**b)
	b = b ^ c
	b = b ^ 3
	
	return b % 8

def brute(v, code):
	if len(code) == 0:
		return v
	
	mi = 1 if v ==0 else 0
	for i in range(mi, 8):
		r = v << 3
		r |= i
		
		if calc(r) == code[-1]:
			
			n = brute(r, code[:-1])
			if n is not None:
				return n
		
	return None
	

def part2():
	res = brute(0, code)
	
	r2 = regs[:]
	r2[0] = res
	r, o = run(r2, code)
	
	assert code == o
	
	return res


p1()
p2()
