from itertools import permutations

from util import input_handler, amplifier_circuit

lines = input_handler.get_input(7)

instr = list(map(int, lines[0].split(",")))

cbs1 = permutations([0, 1, 2, 3, 4])

max_output = -1
part_1_phase_setting = []
for phase_setting in list(cbs1):
    output = 0

    dispatcher_1 = amplifier_circuit.Dispatcher(instr, 5, [1, 4, 0, 3, 2])
    dispatcher_1.start(0)

    if dispatcher_1.get_output()[0] > max_output:
        max_output = dispatcher_1.get_output()[0]
        part_1_phase_setting = phase_setting

print("Part 1: ", max_output)
print("Phase setting: ", part_1_phase_setting)

print()

# part 2

cbs2 = permutations([5, 6, 7, 8, 9])

max_output2 = -1
part_2_phase_setting = []
for phase_setting in list(cbs2):
    output = 0

    dispatcher_2 = amplifier_circuit.Dispatcher(instr, 5, [9, 8, 5, 7, 6])
    dispatcher_2.start(0)

    if dispatcher_2.get_output()[-1] > max_output2:
        max_output2 = dispatcher_2.get_output()[-1]
        part_2_phase_setting = phase_setting

print("Part 2: ", max_output2)
print("Phase setting: ", part_2_phase_setting)
