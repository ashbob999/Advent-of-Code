#include "../aocHelper.h"

class Day23 : public BaseDay
{
public:
	Day23() : BaseDay("23") {}

	result_type solve() override
	{
		long long part1 = 0, part2 = 0;

		enum class opcode : int
		{
			nop,
			hlf,
			tpl,
			inc,
			jmp,
			jie,
			jio
		};

		struct operands
		{
			int op1 = 0;
			int op2 = 0;
		};

		struct instruction
		{
			opcode type = opcode::nop;
			operands data;
		};

		array<long long, 2> registers{};

		vector<instruction> instructions;

		// parse input
		while (*input != '\0')
		{
			instruction instr;

			if (*input == 'h') // hlf
			{
				input += 4; // skip 'hlf '
				instr.type = opcode::hlf;
				instr.data.op1 = *input - 'a';
				input++;
			}
			else if (*input == 't') // tpl
			{
				input += 4; // skip 'tpl '
				instr.type = opcode::tpl;
				instr.data.op1 = *input - 'a';
				input++;
			}
			else if (*input == 'i') // inc
			{
				input += 4; // skip 'inc '
				instr.type = opcode::inc;
				instr.data.op1 = *input - 'a';
				input++;
			}
			else if (*input == 'j')
			{
				input++;
				if (*input == 'm') // jmp
				{
					input += 3; // skip 'mp '
					instr.type = opcode::jmp;
					bool neg = (*input == '-');
					input++;
					instr.data.op1 = numericParse<int>(input);
					if (neg)
					{
						instr.data.op1 *= -1;
					}
				}
				else if (*input == 'i')
				{
					input++;
					if (*input == 'e') // jie
					{
						input += 2; // skip 'e '
						instr.type = opcode::jie;
						instr.data.op1 = *input - 'a';
						input += 3;

						bool neg = (*input == '-');
						input++;
						instr.data.op2 = numericParse<int>(input);
						if (neg)
						{
							instr.data.op2 *= -1;
						}
					}
					else if (*input == 'o') // jio
					{
						input += 2; // skip 'o '
						instr.type = opcode::jio;
						instr.data.op1 = *input - 'a';
						input += 3;

						bool neg = (*input == '-');
						input++;
						instr.data.op2 = numericParse<int>(input);
						if (neg)
						{
							instr.data.op2 *= -1;
						}
					}
				}
			}

			instructions.push_back(instr);

			input++; // skip \n
		}

		auto run_vm = [](array<long long, 2>& registers, vector<instruction>& instructions)
		{
			int pc = 0;

			while (true)
			{
				if (pc < 0 || pc >= instructions.size())
				{
					break;
				}

				instruction& instr = instructions[pc];

				switch (instr.type)
				{
					case opcode::nop:
					{
						cout << "nop" << endl;
						pc++;
						break;
					}
					case opcode::hlf:
					{
						registers[instr.data.op1] /= 2;
						pc++;
						break;
					}
					case opcode::tpl:
					{
						registers[instr.data.op1] *= 3;
						pc++;
						break;
					}
					case opcode::inc:
					{
						registers[instr.data.op1]++;
						pc++;
						break;
					}
					case opcode::jmp:
					{
						pc += instr.data.op1;
						break;
					}
					case opcode::jie:
					{
						if (registers[instr.data.op1] % 2 == 0)
						{
							pc += instr.data.op2;
						}
						else
						{
							pc++;
						}
						break;
					}
					case opcode::jio:
					{
						if (registers[instr.data.op1] == 1)
						{
							pc += instr.data.op2;
						}
						else
						{
							pc++;
						}
						break;
					}
				}
			}
		};

		// part 1
		run_vm(registers, instructions);

		part1 = registers[1];

		// part 2
		registers = { 1, 0 };
		run_vm(registers, instructions);

		part2 = registers[1];

		return { part1, part2 };
	}
};
