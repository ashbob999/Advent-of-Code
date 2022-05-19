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
	get_input_file()
# @formatter:on

from utils import parsefile

input_text = parsefile(file_name, ["\n"])

instr = [line.split(" ") for line in input_text]

from vm import VM_v2, VM_v3


def part1():
	vm = VM_v2(instr)

	vm.registers["a"] = 7

	vm.run()
	return vm.registers["a"]


modified_input = []

loop1_2 = """cpy b c
mul a c d
cpy 0 c
cpy 0 d""".split("\n")

loop3 = """mul c 2 c
cpy 0 d""".split("\n")

modified_jnz = "jnz 1 -13".split("\n")

modified_input += input_text[0:0 + 4]
modified_input += loop1_2
modified_input += input_text[10:10 + 3]
modified_input += loop3
modified_input += input_text[16:16 + 2]
modified_input += modified_jnz
modified_input += input_text[19:19 + 7]

modified_instr = [line.split(" ") for line in modified_input]


def part2():
	vm = VM_v3(modified_instr)

	vm.registers["a"] = 12

	vm.run()
	return vm.registers["a"]


p1()
p2()

"""
part 2 loops

cpy a b
dec b
cpy a d    >4
cpy 0 a
cpy b c    >2 c=b; d=0; a+=c*d; c=0
inc a      >1 a+=c; c=0
dec c
jnz c -2   <1
dec d
jnz d -5   <2
dec b
cpy b c
cpy c d
dec d      >3 c+=d; d=0
inc c
jnz d -2   <3 
tgl c
cpy -16 c
jnz 1 c   #<4
cpy 98 c
jnz 86 d  #>6
inc a      >5
inc d     #
jnz d -2   <5
inc c     #
jnz c -5   <6

loops as functions

func 1 {
	do {
		a++
		c--
	} while c > 0
}

func 1a {
	a+=c
	c=0
}

func 2 {
	c=b
	do {
		func 1()
		d--
	} while d > 0
}

func 2a {
	c=b
	a+=c*d
	c=0
	d=0
}

func 3 {
	do {
		d--
		c++
	} while d > 0
}

func 3a {
	c+=d
	d=0
}

func 4 {
	do {
		d=a
		a=0
		func 2()
		b--
		c=b
		d=c
		func 3()
		toggle c
		if c == 2
			break
		c = -16
	} while true
}

func 4a {
	do {
		d=a
		a=0
		
		c=b
		a+=c*d
		c=0
		d=0
		
		b--
		c=b
		d=c
		
		c+=d # c=2*c
		d=0
		
		toggle c
		if c == 2
			break
		c = -16
	} while true
}

"""
