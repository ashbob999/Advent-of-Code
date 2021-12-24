from os.path import isfile, join as path_join
from sys import path as sys_path
sys_path.insert(1, path_join(sys_path[0], '..'))
file_name = path_join('input', 'day24.txt')
def to_list(mf: object = int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]
def to_gen(mf: object = int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)
def p1(*args): ans = part1(*args); print(ans); return ans
def p2(*args): ans = part2(*args); print(ans); return ans

if not isfile(file_name):
	from aoc import get_input_file
	get_input_file(session_path=['..', '.env'])

from utils import parsefile

instr = parsefile(file_name, [[str, str, 0, " "], "\n"])

def run(instr, inputs):
	regs = {"w":0, "x":0, "y":0, "z":0}
	
	for i in instr:
		op = i[0]
		if op == "inp":
			regs[i[1]] = inputs.pop(0)
		elif op == "add":
			if i[2].lstrip("-").isnumeric():
				regs[i[1]] += int(i[2])
			else:
				regs[i[1]] += regs[i[2]]
		elif op == "mul":
			if i[2].lstrip("-").isnumeric():
				regs[i[1]] *= int(i[2])
			else:
				regs[i[1]] *= regs[i[2]]
		elif op == "div":
			if i[2].lstrip("-").isnumeric():
				if int(i[2]) == 0:
					return False
				regs[i[1]] = int(regs[i[1]] / int(i[2]))
			else:
				if regs[i[2]] == 0:
					return False
				regs[i[1]] = int(regs[i[1]] / regs[i[2]])
		elif op == "mod":
			if regs[i[1]] < 0:
				return False
			if i[2].lstrip("-").isnumeric():
				if int(i[2]) <= 0:
					return False
				regs[i[1]] %= int(i[2])
			else:
				if regs[i[2]] <= 0:
					return False
				regs[i[1]] %= regs[i[2]]
		elif op == "eql":
			if i[2].lstrip("-").isnumeric():
				if regs[i[1]] == int(i[2]):
					regs[i[1]] = 1
				else:
					regs[i[1]] = 0
			else:
				if regs[i[1]] == regs[i[2]]:
					regs[i[1]] = 1
				else:
					regs[i[1]] = 0
					
	return regs["z"] == 0, regs

def do_calc(inp, n, i, z):
	
	x_mod = int(inp[i*18 +3][2])
	z_div = int(inp[i*18 +4][2])
	x_add = int(inp[i*18 +5][2])
	y_add1 = int(inp[i*18 +9][2])
	y_add2 = int(inp[i*18 +11][2])
	y_add3 = int(inp[i*18 + 15][2])
	
	#print(x_mod, z_div, x_add, y_add1, y_add2, y_add3)
	
	w = n
	x = z % z_div
	z = int(z / z_div)
	x += x_add
	x += w
	x = 1 if x==w else 0
	x = 1 if x==0 else 0
	y = y_add1
	y *= x
	y += y_add2
	z *= y
	y = w + y_add3
	y *= x
	z += y
	
	return z

def find_value(inp, n):
	"""
w = inp
x = z%26
z /= 1
x += 15
x += w
x = x==w
x = x==0
y = 25
y *= x
y += 1
z *= y
y = w+9
y *= x
z += y

y == 0
x == 0
	"""
	pass

inp_len = 14
print(len(instr), len(instr) / 18)

def brute(instr):
	inp = int("9"*14)
	#inp = int("1"*14)
	sdv = int("1" + "0"*13)
	while True:
		z = 0
		div_value = sdv
		for i in range(0, 14):
			z = do_calc(instr, (inp // div_value) % 10, i, z)
			#print(z)
			#print((inp // div_value) % 10)
			div_value //= 10
		if z ==0:
			if "0" not in str(inp):
				return inp
			
		#return z
		if inp % 10000 == 0:print(inp, z)
		inp -= 1

def part1():
	
	
	inps = [1]*inp_len
	
	res, regs = run(instr, inps)
	
	"""
	print(res, regs)
	z = 0
	for i in range(0, 14):
		z = do_calc(instr, 1, i, z)
		print(z)
	"""
	
	print(brute(instr))

"""
w = inp
x = z%26
z /= 1
x += 15
x += w
x = x==w
x = x==0
y = 25
y *= x
y += 1
z *= y
y = w+9
y *= x
z += y

inp w
mul x 0
add x z
mod x 26
div z 1
add x 15
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 9
mul y x
add z y
"""


def part2():
	pass


p1()
p2()
