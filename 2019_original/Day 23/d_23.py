from ic import Computer


def run_network():
	with open('Data_23.txt') as infile:
		program = list(map(int, infile.read().split(',')))
	computers = {}
	programs = {}
	for address in range(50):
		computer = Computer(program)
		computer.set_input([address])
		computers[address] = computer
		programs[address] = computer.run_program()
	messages = {address: [] for address in range(50)}
	nat_value = None
	nat_y_sent = set()
	while True:
		for address, program in programs.items():
			output = next(program)
			if output is not None:
				messages[address].append(output)
				if len(messages[address]) == 3:
					destination, x, y = messages.pop(address)
					if destination == 255:
						nat_value = (x, y)
					else:
						computers[destination].set_input((x, y))
					messages[address] = []
			idle = (sum(len(computer.inputs) for computer in
			            computers.values()) == 0)
			if idle and nat_value:
				computers[0].set_input(nat_value)
				y = nat_value[1]
				print(y)
				if y in nat_y_sent:
					return y
				nat_y_sent.add(y)
				nat_value = None


result = run_network()
print(result)
