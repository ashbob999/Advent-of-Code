from __future__ import annotations

"""
with open("Day 09/Data_09.txt", "r") as file:
	lines = [line.strip() for line in file]

instr = list(map(int, lines[0].split(",")))
#instr[1] = 12
#instr[2] = 2
"""


class IntCodeVM:
    def __init__(self, instructions, inputs):

        self.instructions = instructions.copy()

        self.opcode_params = {
            "01": 3,
            "02": 3,
            "03": 1,
            "04": 1,
            "05": 2,
            "06": 2,
            "07": 3,
            "08": 3,
            "09": 1,
            "99": 0
        }

        self.inputs = inputs

        # opcodes 1,2 are represented by ABCDE, ABC type of params, DE is the opcode

        # Part 1

        self.program_outputs = []
        self.running = False

        self.disp = None

        self.rel_base = 0

        self.pc = 0

    def run(self):
        self.running = True

        while self.running:
            # print(self.pc)
            # print(self.instructions[self.pc:self.pc+3])
            # print("226: ", self.instructions[226], "  677: ", self.instructions[677])

            instruction = str(self.instructions[self.pc]).rjust(5, "0")  # pads out the instruction

            opcode = instruction[-2:]
            param_modes = instruction[:-2]
            # print(opcode, "  :  ", self.pc)
            # print("opcode ", opcode)
            # pc_1 = self.pc+1
            # pc_x = self.pc +1 +self.opcode_params[opcode]

            # params = self.instructions[pc_1:pc_x]
            params = self.instructions[self.pc + 1:self.pc + 1 + self.opcode_params[opcode]]

            addrs = self.get_addresses(params, param_modes)

            if opcode == "01":  # adds
                # print("adds:")
                # value1 = params[0] if param_modes[2] == "1" else self.instructions[params[0]]
                # value2 = params[1] if param_modes[1] == "1" else self.instructions[params[1]]
                # store_location = params[2]

                value1 = self.instructions[addrs[0]]
                value2 = self.instructions[addrs[1]]
                store_location = addrs[2]

                # self.instructions[store_location] = value1 + value2
                self.instructions[store_location] = value1 + value2
            elif opcode == "02":  # multiplies
                # print("mults")
                # value1 = params[0] if param_modes[2] == "1" else self.instructions[params[0]]
                # value2 = params[1] if param_modes[1] == "1" else self.instructions[params[1]]
                # store_location = params[2]

                value1 = self.instructions[addrs[0]]
                value2 = self.instructions[addrs[1]]
                store_location = addrs[2]

                # self.instructions[store_location] = value1 * value2
                self.instructions[store_location] = value1 * value2
            elif opcode == "03":  # input
                # print(self.id, "  input: ", self.inputs)

                if len(self.inputs) == 0:
                    self.running = False
                    return

                # self.instructions[params[0]] = self.inputs.pop(0)
                self.instructions[addrs[0]] = self.inputs.pop(0)
            elif opcode == "04":  # output
                # print("output", self.disp)
                # print(instructions)
                # output_value = params[0] if param_modes[2] == "1" else self.instructions[params[0]]
                output_value = self.instructions[addrs[0]]

                # print("output: ", output_value, "  :  ", addrs[0])
                """
                print(self.id, ":  output:  ", output_value)
                """
                if self.disp is not None:
                    self.disp.pass_output(self, output_value)

                self.program_outputs.append(output_value)
            elif opcode == "05":  # jump-if-true
                # value1 = params[0] if param_modes[2] == "1" else self.instructions[params[0]]
                # next_instruction = params[1] if param_modes[1] == "1" else self.instructions[params[1]]
                value1 = self.instructions[addrs[0]]
                next_instruction = self.instructions[addrs[1]]

                if value1 != 0:
                    self.pc = next_instruction
                    continue
            elif opcode == "06":  # jump-if-false
                # value1 = params[0] if param_modes[2] == "1" else self.instructions[params[0]]
                # next_instruction = params[1] if param_modes[1] == "1" else self.instructions[params[1]]
                value1 = self.instructions[addrs[0]]
                next_instruction = self.instructions[addrs[1]]
                # print("j_f  ", value1, "  :  ", next_instruction)

                if value1 == 0:
                    self.pc = next_instruction
                    continue
            elif opcode == "07":  # less-than
                # value1 = params[0] if param_modes[2] == "1" else self.instructions[params[0]]
                # value2 = params[1] if param_modes[1] == "1" else self.instructions[params[1]]
                # store_location = params[2]
                value1 = self.instructions[addrs[0]]
                value2 = self.instructions[addrs[1]]
                store_location = addrs[2]

                # print("values: ", value1, " : ",value2)
                # print("store: ", store_location, "  : ", value1<value2)
                # self.instructions[store_location] = 1 if value1 < value2 else 0
                self.instructions[store_location] = 1 if value1 < value2 else 0
            elif opcode == "08":  # equals
                # value1 = params[0] if param_modes[2] == "1" else self.instructions[params[0]]
                # value2 = params[1] if param_modes[1] == "1" else self.instructions[params[1]]
                # store_location = params[2]
                value1 = self.instructions[addrs[0]]
                value2 = self.instructions[addrs[1]]
                store_location = addrs[2]

                # self.instructions[store_location] = 1 if value1 == value2 else 0
                self.instructions[store_location] = 1 if value1 == value2 else 0
            elif opcode == "09":
                value1 = self.instructions[addrs[0]]

                self.rel_base += value1

            elif opcode == "99":  # halt
                # print("halt")
                break

            # print("pc: ", self.pc, "  opcode: ", opcode, "  224: ",self.instructions[224])
            self.pc += self.opcode_params[opcode] + 1
        return self.program_outputs

    def add_input(self, value):
        self.inputs.append(value)
        if not self.running:
            self.run()

    def get_addresses(self, params, param_modes):
        p_modes = param_modes[::-1]
        # print("modes ",p_modes)
        addresses = [-1] * len(params)

        for i, param in enumerate(params):
            # i +=1
            if p_modes[i] == "0":
                addresses[i] = param
            elif p_modes[i] == "1":
                addresses[i] = self.pc + i + 1
            elif p_modes[i] == "2":
                addresses[i] = self.rel_base + param

        # print("addrs: ", addresses)
        return addresses

    def set_dispatcher(self, disp):
        self.disp = disp



"""
inputs = []
vm = intcode(instr, inputs)
#vm.run()
print(vm.instructions[0:5])
#3892695
 

phase = (9, 8, 5, 7, 6)
disp = dispatcher(instr, 5, phase)
disp.start(0)
print("\n")
print(disp.get_output())
"""
