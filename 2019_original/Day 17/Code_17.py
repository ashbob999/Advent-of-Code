from intcode import IntCodeVM

with open("Data_17.txt", "r") as file:
	lines = [line.strip() for line in file]

instr = list(map(int, lines[0].split(",")))


def pad_list(arr, amount):
	for i in range(amount):
		arr.append(0)


# part 1

pad_list(instr, len(instr) * 10)

vm = IntCodeVM(instr, [])

vm.run()

outputs = vm.program_outputs

grid_str = ""

for output in outputs:
	if output == 10:  # \n: new line
		grid_str += "\n"
	elif output == 35:  # #: scaffold
		grid_str += "#"
	elif output == 46:  # .: space
		grid_str += "."
	elif chr(output) in ["^", "<", ">", "V"]:
		grid_str += chr(output)

print(grid_str)

grid = [list(row) for row in grid_str.split("\n") if list(row)]

total_alignment = 0

for i in range(1, len(grid) - 1):
	for j in range(1, len(grid[0]) - 1):
		if grid[i][j] == "#":
			if grid[i - 1][j] == "#" and \
					grid[i + 1][j] == "#" and \
					grid[i][j - 1] == "#" and \
					grid[i][j + 1] == "#":
				total_alignment += i * j

print("Part 1: ", total_alignment)

# part 2

main_str = "A,B,A,C,A,B,C,B,C,B\n"
func_a_str = "L,5,5,R,8,L,6,R,6\n"
func_b_str = "L,8,L,8,R,8\n"
func_c_str = "R,8,L,6,L,5,5,L,5,5\n"
video_str = "n\n"

print(len(main_str[:-1]))
print(len(func_a_str[:-1]))
print(len(func_b_str[:-1]))
print(len(func_c_str[:-1]))
print(len(video_str[:-1]))

instr[0] = 2

inputs = \
	[ord(c) for c in list(main_str)] + \
	[ord(c) for c in list(func_a_str)] + \
	[ord(c) for c in list(func_b_str)] + \
	[ord(c) for c in list(func_c_str)] + \
	[ord(c) for c in list(video_str)]

# print(inputs)

vm = IntCodeVM(instr, inputs)

vm.run()

outputs = vm.program_outputs

print("Part 2: ", outputs[-1])
