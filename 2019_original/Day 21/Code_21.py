from intcode import IntCodeVM

with open("Data_21.txt", "r") as file:
	lines = [line.strip() for line in file]

instr = list(map(int, lines[0].split(",")))


def pad_list(arr, amount):
	for i in range(amount):
		arr.append(0)


# part 1

pad_list(instr, len(instr))

# if b or c > jump
# not d

code = [
	"NOT B T",
	"NOT C J",
	"OR T J",
	"AND D J",
	"NOT A T",
	"OR T J",
	"WALK",
]

ascii_instr = []
for i in code:
	ascii_instr += [*[ord(c) for c in list(i)], ord("\n")]

vm = IntCodeVM(instr, ascii_instr)
vm.run()

try:
	print("".join([chr(x) for x in vm.program_outputs]))
except Exception:
	print("Part 1: ", vm.program_outputs[-1])

# part 2

code = [
	"NOT B T",
	"NOT C J",
	"OR T J",
	"AND D J",
	"NOT A T",
	"OR T J",
	"AND T J",
	"NOT E T",
	"NOT T T",
	"AND H T",
	# "NOT T T",
	"AND T J",
	"RUN",
]

# i did D&!(A|B|C)&(E|!H)

ascii_instr = []
for i in code:
	ascii_instr += [*[ord(c) for c in list(i)], ord("\n")]

vm = IntCodeVM(instr, ascii_instr)
vm.run()

try:
	print("".join([chr(x) for x in vm.program_outputs]))
except Exception:
	print("Part 2: ", vm.program_outputs[-1])
