# link to Day 1: https://adventofcode.com/2019/day/5

from util import input_handler, intcode_machine

lines = input_handler.get_input(5)

instructions = list(map(int, lines[0].split(",")))

opcode_params = {
    "01": 3,
    "02": 3,
    "03": 1,
    "04": 1,
    "05": 2,
    "06": 2,
    "07": 3,
    "08": 3,
    "99": 0
}

# opcodes 1,2 are represented by ABCDE, ABC type of params, DE is the opcode

# Part 1

program_input_1 = 1
program_input_2 = 5

program_outputs = []

pc = 0

while pc < len(instructions):
    # print(pc)
    instruction = str(instructions[pc]).rjust(5, "0")  # pads out the instruction

    opcode = instruction[-2:]
    param_modes = instruction[:-2]
    params = instructions[pc + 1:pc + 1 + opcode_params[opcode]]

    if opcode == "01":  # adds
        # print("adds:")
        value1 = params[0] if param_modes[2] == "1" else instructions[params[0]]
        value2 = params[1] if param_modes[1] == "1" else instructions[params[1]]
        store_location = params[2]

        instructions[store_location] = value1 + value2
    elif opcode == "02":  # multiplies
        # print("mults")
        value1 = params[0] if param_modes[2] == "1" else instructions[params[0]]
        value2 = params[1] if param_modes[1] == "1" else instructions[params[1]]
        store_location = params[2]

        instructions[store_location] = value1 * value2
    elif opcode == "03":  # input
        # print("input")
        instructions[params[0]] = program_input_2
    elif opcode == "04":  # output
        # print("output")
        # print(instructions)

        program_outputs.append(params[0] if param_modes[2] == "1" else instructions[params[0]])
    elif opcode == "05":  # jump-if-true
        value1 = params[0] if param_modes[2] == "1" else instructions[params[0]]
        next_instruction = params[1] if param_modes[1] == "1" else instructions[params[1]]

        if value1 != 0:
            pc = next_instruction
            continue
    elif opcode == "06":  # jump-if-false
        value1 = params[0] if param_modes[2] == "1" else instructions[params[0]]
        next_instruction = params[1] if param_modes[1] == "1" else instructions[params[1]]

        if value1 == 0:
            pc = next_instruction
            continue
    elif opcode == "07":  # less-than
        value1 = params[0] if param_modes[2] == "1" else instructions[params[0]]
        value2 = params[1] if param_modes[1] == "1" else instructions[params[1]]
        store_location = params[2]

        instructions[store_location] = 1 if value1 < value2 else 0
    elif opcode == "08":  # equals
        value1 = params[0] if param_modes[2] == "1" else instructions[params[0]]
        value2 = params[1] if param_modes[1] == "1" else instructions[params[1]]
        store_location = params[2]

        instructions[store_location] = 1 if value1 == value2 else 0
    elif opcode == "99":  # halt
        # print("halt")
        break

    pc += opcode_params[opcode] + 1

print(program_outputs)

print("Part 1: ")

# Part 2

print("Part 2: ")

# print("at 0: ", instructions[0])
print("\n" * 3)

ic = intcode_machine.IntCodeVM(list(map(int, lines[0].split(","))))

ic.set_input([1])

ic.run()

print(ic.outputs)
