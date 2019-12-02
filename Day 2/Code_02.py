import math

# gets the input lines for the challenge
with open("Data_02.txt", "r") as file:
	lines = [line.strip() for line in file]

preserved_opcodes =  [int(code) for code in lines[0].split(",")]
		
opcodes = preserved_opcodes.copy()

# Part 1

opcodes[1] = 12
opcodes[2] = 2

def calc_opcodes(ops):
	for i in range(0, len(ops), 4):
		opcode = ops[i]
	
		if opcode == 1:
			value1 = ops[ops[i+1]]
			value2 = ops[ops[i+2]]
			storeLocation = ops[i+3]
		
			ops[storeLocation] = value1 + value2
		elif opcode == 2:
			value1 = ops[ops[i+1]]
			value2 = ops[ops[i+2]]
			storeLocation = ops[i+3]
		
			ops[storeLocation] = value1 * value2
		elif opcode == 99:
			return ops
	return ops
	
opcodes = calc_opcodes(opcodes)
		
print("Value at Index 0: ", opcodes[0])

# Part 2 (bruteforce solution)

desired_output = 19690720
correct_noun = 0
correct_verb = 0

for noun in range(0, 100):
	for verb in range(0, 100):
		current_opcodes = preserved_opcodes.copy()
		current_opcodes[1] = noun
		current_opcodes[2] = verb
		new_opcodes = calc_opcodes(current_opcodes)
		if new_opcodes[0] == desired_output:
			correct_noun = noun
			correct_verb = verb
			break

print("Part 2")
print("Noun: ", correct_noun)
print("Verb: ", correct_verb)
print("Value: ", 100* correct_noun + correct_verb)