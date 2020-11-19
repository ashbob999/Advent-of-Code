from intcode import IntCodeVM

with open("Data_23.txt", "r") as file:
	lines = [line.strip() for line in file]

instr = list(map(int, lines[0].split(",")))


def pad_list(arr, amount):
	for i in range(amount):
		arr.append(0)


# part 1

pad_list(instr, len(instr) * 5)

network = [IntCodeVM(instr, [i]) for i in range(50)]

packet_queue = {i: [] for i in range(50)}
packet_queue[255] = []

for vm in network:
	vm.run()

while packet_queue[255] == []:

	for i, vm in enumerate(network):
		if len(vm.program_outputs) % 3 == 0:
			while len(vm.program_outputs) > 0:
				packet = vm.program_outputs[-3:]
				destination = packet[0]
				data = tuple(packet[1:])

				packet_queue[destination].append(data)

				vm.program_outputs.pop()
				vm.program_outputs.pop()
				vm.program_outputs.pop()

	for i, vm in enumerate(network):
		if len(packet_queue[i]) == 0:
			vm.add_input(-1)
		else:
			while len(packet_queue[i]) > 0:
				data = packet_queue[i].pop(0)
				vm.add_input(data[0])
				vm.add_input(data[1])

print("Part 1: ", packet_queue[255][0][1])

# part 2

network = [IntCodeVM(instr, [i]) for i in range(50)]

packet_queue = {i: [] for i in range(50)}
packet_queue[255] = None

for vm in network:
	vm.run()

nat_y_delivered = [0, None]

while nat_y_delivered[-1] != nat_y_delivered[-2]:

	for i, vm in enumerate(network):
		if len(vm.program_outputs) % 3 == 0:
			if len(vm.program_outputs) > 0:
				packet = vm.program_outputs[-3:]
				destination = packet[0]
				data = tuple(packet[1:])

				if destination == 255:
					packet_queue[destination] = data
				else:
					packet_queue[destination].append(data)

				vm.program_outputs.pop()
				vm.program_outputs.pop()
				vm.program_outputs.pop()

	is_idle = True
	for i, vm in enumerate(network):
		if len(packet_queue[i]) == 0:
			vm.add_input(-1)
		else:
			is_idle = False
			while len(packet_queue[i]) > 0:
				data = packet_queue[i].pop(0)
				vm.add_input(data[0])
				vm.add_input(data[1])

	if is_idle:
		data = packet_queue[255]
		if data != None:
			network[0].add_input(data[0])
			network[0].add_input(data[1])

			print("idle, y: ", data[1])
			nat_y_delivered.append(data[1])
			packet_queue[255] = None

print("Part 2: ", nat_y_delivered[-1])
