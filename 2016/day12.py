# @formatter:off
from os.path import isfile, join as path_join
from sys import path as sys_path
sys_path.insert(1, path_join(sys_path[0], '..'))
file_name = path_join('input', 'day12.txt')
def to_list(mf: object = int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]
def to_gen(mf: object = int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)
def p1(*args): ans = part1(*args); print(ans); return ans
def p2(*args): ans = part2(*args); print(ans); return ans

if not isfile(file_name):
	from aoc import get_input_file
	get_input_file()
# @formatter:on

from utils import parsefile

instr = parsefile(file_name, [[" "], "\n"])

from vm import VM


def part1():
	vm = VM(instr)

	vm.run()
	return vm.registers["a"]


def part2():
	vm = VM(instr)
	vm.registers["c"] = 1

	vm.run()
	return vm.registers["a"]


p1()
p2()
