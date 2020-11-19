from intcode import IntCodeVM

with open("Data_19.txt", "r") as file:
	lines = [line.strip() for line in file]

instr = list(map(int, lines[0].split(",")))


def pad_list(arr, amount):
	for i in range(amount):
		arr.append(0)


# part 1

pad_list(instr, len(instr))

affected = set()

for x in range(50):
	for y in range(50):
		inp = [x, y]
		# print(x,y)
		vm = IntCodeVM(instr, [x, y])
		vm.run()
		output = vm.program_outputs[-1]
		# print(vm.program_outputs)
		if output == 1:
			affected.add(tuple([x, y]))
	if x % 10 == 0:
		print(x)

print("Part 1: ", len(affected))

g = [["." for x in range(50)] for y in range(50)]

for p in affected:
	g[p[1]][p[0]] = "#"

print()
for r in g:
	# break
	print("".join(r))


# part 2

def check_beam(pos):
	vm = IntCodeVM(instr, list(pos))
	vm.run()
	if vm.program_outputs[0] == 1:
		return True
	else:
		return False


found = False

x_pos = 0
top_left = None

while not found and x_pos < 2000:
	y_pos = x_pos + (x_pos // 16) + 2
	# print(x_pos, y_pos)
	if check_beam((x_pos, y_pos)):
		new_x_pos = x_pos - 99
		new_y_pos = y_pos + 99
		if x_pos == 890 and y_pos == 946:
			print("at tl: ", new_x_pos, new_y_pos)
		if new_x_pos >= 0 and new_y_pos >= 0:
			if check_beam((new_x_pos, new_y_pos)):
				print("100x100", new_x_pos, y_pos)
				top_left = (new_x_pos, y_pos)
				found = True

	if x_pos % 200 == 0:
		print("x ", x_pos)

	x_pos += 1

print("Part 2: ", top_left[0] * 10000 + top_left[1])
