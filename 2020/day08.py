from typing import Callable
from os.path import isfile, join as path_join
file_name = path_join('input', 'day08.txt')
def to_list(mf: Callable = int, sep='\n'): return [mf(x) for x in open(file_name).read().split(sep) if x]
def to_gen(mf: Callable = int, sep='\n'): return (mf(x) for x in open(file_name).read().split(sep) if x)

if not isfile(file_name):
	from aoc import get_input_file
	get_input_file(session_path=['..', '.env'])

data = to_list(mf=str)
instr_ = [[x.split(" ")[0], int(x.split(" ")[1])] for x in data]

def part1(instr):
	seen = set()

	pc = 0
	acc = 0

	while True:
		if pc == len(instr):
			return (True, acc)
		if pc in seen:
			return (False, acc)
		seen.add(pc)
		if instr[pc][0] == "nop":
			pc += 1
		elif instr[pc][0] == "acc":
			acc += instr[pc][1]
			pc += 1
		elif instr[pc][0] == "jmp":
			pc += instr[pc][1]


def part2():
	change_i = 0
	for i in range(len(data)):
		if instr_[i][0] == "acc":
			continue
		data2 = to_list(mf=str)
		instr2 = [[x.split(" ")[0], int(x.split(" ")[1])] for x in data]

		if instr2[i][0] == "jmp":
			instr2[i][0] = "nop"
		elif instr2[i][0] == "nop":
			instr2[i][0] = "jmp"

		res = part1(instr2)
		if res[0]:
			return res


print(part1(instr_))
print(part2())
