from __future__ import annotations

from typing import List, Dict

from util import amplifier_circuit


class IntCodeVM:
    def __init__(self, instructions: List[int], inputs: List[int]) -> None:

        self.instructions: list[int] = instructions.copy()

        self.opcode_params: Dict[str, int] = {
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

        self.inputs: List[int] = inputs

        # opcodes 1,2 are represented by ABCDE, ABC type of params, DE is the opcode

        # Part 1

        self.program_outputs: List[int] = []
        self.running: bool = False
        self.finished: bool = False

        self.dispatcher = None

        self.rel_base: int = 0

        self.pc: int = 0

    def run(self):
        self.running = True

        while self.running:

            instruction: str = str(self.instructions[self.pc]).rjust(5, "0")  # pads out the instruction

            opcode: str = instruction[-2:]
            param_modes: str = instruction[:-2]

            params: List[int] = self.instructions[self.pc + 1:self.pc + 1 + self.opcode_params[opcode]]

            addresses: List[int] = self.get_addresses(params, param_modes)

            if opcode == "01":  # adds
                value1 = self.instructions[addresses[0]]
                value2 = self.instructions[addresses[1]]
                store_location = addresses[2]

                self.instructions[store_location] = value1 + value2
            elif opcode == "02":  # multiplies
                value1 = self.instructions[addresses[0]]
                value2 = self.instructions[addresses[1]]
                store_location = addresses[2]

                self.instructions[store_location] = value1 * value2
            elif opcode == "03":  # input
                if len(self.inputs) == 0:
                    self.running = False
                    return None

                self.instructions[addresses[0]] = self.inputs.pop(0)
            elif opcode == "04":  # output
                output_value = self.instructions[addresses[0]]

                if self.dispatcher is not None:
                    self.dispatcher.pass_output(self, output_value)

                self.program_outputs.append(output_value)
            elif opcode == "05":  # jump-if-true
                value1 = self.instructions[addresses[0]]
                next_instruction = self.instructions[addresses[1]]

                if value1 != 0:
                    self.pc = next_instruction
                    continue
            elif opcode == "06":  # jump-if-false
                value1 = self.instructions[addresses[0]]
                next_instruction = self.instructions[addresses[1]]

                if value1 == 0:
                    self.pc = next_instruction
                    continue
            elif opcode == "07":  # less-than
                value1 = self.instructions[addresses[0]]
                value2 = self.instructions[addresses[1]]
                store_location = addresses[2]

                self.instructions[store_location] = 1 if value1 < value2 else 0
            elif opcode == "08":  # equals
                value1 = self.instructions[addresses[0]]
                value2 = self.instructions[addresses[1]]
                store_location = addresses[2]

                self.instructions[store_location] = 1 if value1 == value2 else 0
            elif opcode == "09":
                value1 = self.instructions[addresses[0]]

                self.rel_base += value1

            elif opcode == "99":  # halt
                self.finished = True
                break

            self.pc += self.opcode_params[opcode] + 1
        return self.program_outputs

    def add_input(self, value):
        self.inputs.append(value)
        if not self.running:
            self.run()

    def get_addresses(self, params, param_modes):
        p_modes = param_modes[::-1]
        addresses = [-1] * len(params)

        for i, param in enumerate(params):
            # i +=1
            if p_modes[i] == "0":
                addresses[i] = param
            elif p_modes[i] == "1":
                addresses[i] = self.pc + i + 1
            elif p_modes[i] == "2":
                addresses[i] = self.rel_base + param

        return addresses

    def set_dispatcher(self, disp: amplifier_circuit.Dispatcher):
        self.dispatcher = disp
