from aoc import input_handler

# gets the input lines for the challenge
lines = input_handler.get_input(2)

preserved_opcodes = [int(code) for code in lines[0].split(",")]

opcodes = preserved_opcodes.copy()

# Part 1

opcodes[1] = 12
opcodes[2] = 2


def calc_opcodes(ops):
    for i in range(0, len(ops), 4):
        opcode = ops[i]

        if opcode == 1:
            value1 = ops[ops[i + 1]]
            value2 = ops[ops[i + 2]]
            store_location = ops[i + 3]

            ops[store_location] = value1 + value2
        elif opcode == 2:
            value1 = ops[ops[i + 1]]
            value2 = ops[ops[i + 2]]
            store_location = ops[i + 3]

            ops[store_location] = value1 * value2
        elif opcode == 99:
            return ops
    return ops


opcodes = calc_opcodes(opcodes)

print("Part 1: Value at Index 0: ", opcodes[0])

# Part 2 (brute force solution)

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
print("Value: ", 100 * correct_noun + correct_verb)
