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
	regs = {"w": 0, "x": 0, "y": 0, "z": 0}

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
	x_mod = 26  # int(inp[i * 18 + 3][2])
	z_div = int(inp[i * 18 + 4][2])
	x_add = int(inp[i * 18 + 5][2])
	y_add1 = 25  # int(inp[i * 18 + 9][2])
	y_add2 = 1  # int(inp[i * 18 + 11][2])
	y_add3 = int(inp[i * 18 + 15][2])

	# print(x_mod, z_div, x_add, y_add1, y_add2, y_add3)

	w = n
	x = z % 26  # x_mod
	z = int(z / z_div)
	x += x_add
	x += w
	# x = 1 if x == w else 0
	# x = 1 if x == 0 else 0
	x = 1 if x != w else 0
	y = 25  # y_add1
	y *= x
	y += 1  # y_add2
	z *= y
	y = w + y_add3
	y *= x
	z += y

	return z


from ctypes import *

func = CDLL("./func.so")


def do_calc2(inp, n, i, z):
	z_div = int(inp[i * 18 + 4][2])
	x_add = int(inp[i * 18 + 5][2])
	y_add = int(inp[i * 18 + 15][2])

	return func.calc(n, z, z_div, x_add, y_add)


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
	inp = int("9" * 14)
	# inp = int("1"*14)
	sdv = int("1" + "0" * 13)
	while True:
		z = 0
		div_value = sdv
		for i in range(0, 14):
			z = do_calc(instr, (inp // div_value) % 10, i, z)
			# print(z)
			# print((inp // div_value) % 10)
			div_value //= 10
		if z == 0:
			if "0" not in str(inp):
				return inp

		# return z
		if inp % 10000 == 0: print(inp, z)
		inp -= 1


def get_z_start(instr, index, end_value):
	for i in range(9, 0, -1):
		z = 0
		out_z = -1
		# out_z != 0 and
		while z < 1000000:
			z += 1
			out_z = do_calc(instr, i, index, z)
			if out_z == 0:
				yield i, z, out_z
				break

	yield None, None, None


def part1():
	inps = [1] * inp_len

	res, regs = run(instr, inps)

	print(res, regs)
	z = 0
	for i in range(0, 14):
		z = do_calc(instr, 1, i, z)
		print(z)

	print()

	# for i in range(1, 10):
	# 	z = 0
	# 	out_z = -1
	# 	# out_z != 0 and
	# 	while z < 100000:
	# 		z += 1
	# 		out_z = do_calc(instr, i, 13, z)
	# 		if out_z == 0: print(i, z, out_z)
	#
	# 	if out_z == 0: print("found zero", i, z)

	print(do_calc(instr, 9, 13, 2))
	print(do_calc2(instr, 9, 13, 2))

	# print(get_z_start(instr, 13, 0))

	# nums = []
	# reses = []
	# res = (None, 0, None)
	# for i in range(13, 0, -1):
	# 	res = get_z_start(instr, i, res[1])
	# 	print("set", i, res)
	# 	if res[0] is None:
	# 		print("no valid value")
	# 		break
	# 	nums.append(res[0])
	# 	reses.append(res)

	# print(nums)

	from timeit import timeit
	def f():
		do_calc(instr, 9, 13, 2)

	def f2():
		do_calc2(instr, 9, 13, 2)

	print(timeit(f, number=1000) * 1000)
	print(timeit(f2, number=1000) * 1000)

	# print(brute(instr))

	return 0


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
