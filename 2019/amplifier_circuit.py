import intcode_machine


class Dispatcher:
    def __init__(self, instructions, amp_num, amp_phase):
        self.amp_num = amp_num
        self.amp_phase = amp_num

        self.vms = [None] * amp_num

        for i, v in enumerate(amp_phase):
            self.vms[i] = intcode_machine.IntCodeVM(instructions, [v])
            self.vms[i].set_dispatcher(self)

    def start(self, input: int = 0):
        self.vms[0].inputs.append(input)

        for vm in self.vms:
            vm.run()

    def get_output(self):
        return self.vms[-1].program_outputs

    def pass_output(self, vm, output):
        vm_index = self.vms.index(vm)
        # print("passing: ", output, " from ", vm_index, " to ", vm_index+1)
        self.vms[(vm_index + 1) % len(self.vms)].add_input(output)
