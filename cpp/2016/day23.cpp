#include "../aocHelper.h"

#include "vm.h"

class Day23 : public BaseDay
{
public:
	Day23() : BaseDay("23") {}

	result_type solve() override
	{
		long long part1 = 0, part2 = 0;

		VM vm{ input };

		// part 1
		vm.registers['a'] = 7;
		vm.run();
		part1 = vm.registers['a'];

		// part 2
		// modify instructions to use a multiply instead of nested loops
		vector<VM::Instruction> loop_1_2;
		// cpy b c
		loop_1_2.push_back({ VM::Opcode::CPY, {{VM::Operand::Register, 'b'}, {VM::Operand::Register, 'c'}} });
		// mul a c d
		loop_1_2.push_back({ VM::Opcode::MUL, {{VM::Operand::Register, 'a'}, {VM::Operand::Register, 'c'}, {VM::Operand::Register, 'd'}} });
		// cpy 0 c
		loop_1_2.push_back({ VM::Opcode::CPY, {{VM::Operand::Number, 0}, {VM::Operand::Register, 'c'}} });
		// cpy 0 d
		loop_1_2.push_back({ VM::Opcode::CPY, {{VM::Operand::Number, 0}, {VM::Operand::Register, 'd'}} });

		vector<VM::Instruction> loop_3;
		// mul c 2 c
		loop_3.push_back({ VM::Opcode::MUL, {{VM::Operand::Register, 'c'}, {VM::Operand::Number, 2}, {VM::Operand::Register, 'c'}} });
		// cpy 0 d
		loop_3.push_back({ VM::Opcode::CPY, {{VM::Operand::Number, 0}, {VM::Operand::Register, 'd'}} });

		// jnz 1 13
		VM::Instruction modified_jnz{ VM::Opcode::JNZ, {{VM::Operand::Number, 1}, {VM::Operand::Number, -13}} };

		vector<VM::Instruction> instructions;
		instructions.insert(instructions.end(), vm.instructions.begin(), vm.instructions.begin() + 4);
		instructions.insert(instructions.end(), loop_1_2.begin(), loop_1_2.end());
		instructions.insert(instructions.end(), vm.instructions.begin() + 10, vm.instructions.begin() + 10 + 3);
		instructions.insert(instructions.end(), loop_3.begin(), loop_3.end());
		instructions.insert(instructions.end(), vm.instructions.begin() + 16, vm.instructions.begin() + 16 + 2);
		instructions.push_back(modified_jnz);
		instructions.insert(instructions.end(), vm.instructions.begin() + 19, vm.instructions.begin() + 19 + 7);

		vm.reset();
		vm.instructions = instructions;
		vm.registers['a'] = 12;
		vm.run();
		part2 = vm.registers['a'];

		return { part1, part2 };
	}
};
