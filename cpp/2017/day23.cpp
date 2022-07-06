#include "../aocHelper.h"

class Day23 : public BaseDay
{
public:
	Day23() : BaseDay("23") {}

	result_type solve() override
	{
		long long part1 = 0, part2 = 0;

		class VM
		{
		public:
			enum class op_type
			{
				set,
				sub,
				mul,
				jnz,
			};

			struct instr
			{
				op_type op;
				char reg1 = 0;
				int value1 = '\0';
				char reg2 = 0;
				int value2 = '\0';
			};

			vector<instr>& instructions;
			int pc = 0;
			int mul_count = 0;
			unordered_map<char, int> registers;
		public:
			VM(vector<instr>& instructions) : instructions(instructions)
			{
				for (int i = 'a'; i < 'h'; i++)
				{
					registers[(char) i] = 0;
				}
			}

			void run()
			{
				while (pc >= 0 && pc < instructions.size())
				{
					instr& inst = instructions[pc];

					switch (inst.op)
					{
						case op_type::set:
						{
							int value;
							if (inst.reg2 == '\0')
							{
								value = inst.value2;
							}
							else
							{
								value = registers[inst.reg2];
							}

							registers[inst.reg1] = value;

							pc++;
							break;
						}
						case op_type::sub:
						{
							int value;
							if (inst.reg2 == '\0')
							{
								value = inst.value2;
							}
							else
							{
								value = registers[inst.reg2];
							}

							registers[inst.reg1] -= value;

							pc++;
							break;
						}
						case op_type::mul:
						{
							int value;
							if (inst.reg2 == '\0')
							{
								value = inst.value2;
							}
							else
							{
								value = registers[inst.reg2];
							}

							registers[inst.reg1] *= value;
							mul_count++;

							pc++;
							break;
						}
						case op_type::jnz:
						{
							int value;
							if (inst.reg1 == '\0')
							{
								value = inst.value1;
							}
							else
							{
								value = registers[inst.reg1];
							}

							int offset;
							if (inst.reg2 == '\0')
							{
								offset = inst.value2;
							}
							else
							{
								offset = registers[inst.reg2];
							}

							if (value != 0)
							{
								pc += offset;
							}
							else
							{
								pc++;
							}

							break;
						}
					}
				}
			}
		};

		vector<VM::instr> instructions;

		// parse input
		while (*input != '\0')
		{
			VM::instr inst;

			if (*input == 's')
			{
				input++; // skip 's'
				if (*input == 'e') // set
				{
					inst.op = VM::op_type::set;
					input += 3; // skip "et "
					inst.reg1 = *input;
					input += 2;
					if (*input >= 'a' && *input <= 'z')
					{
						inst.reg2 = *input;
						input++;
					}
					else
					{
						inst.value2 = numericParse<int>(input);
					}
				}
				else // sub
				{
					inst.op = VM::op_type::sub;
					input += 3; // skip "ub "
					inst.reg1 = *input;
					input += 2;
					if (*input >= 'a' && *input <= 'z')
					{
						inst.reg2 = *input;
						input++;
					}
					else
					{
						inst.value2 = numericParse<int>(input);
					}
				}
			}
			else if (*input == 'm') // mul
			{
				inst.op = VM::op_type::mul;
				input += 4; // skip "mul "
				inst.reg1 = *input;
				input += 2;
				if (*input >= 'a' && *input <= 'z')
				{
					inst.reg2 = *input;
					input++;
				}
				else
				{
					inst.value2 = numericParse<int>(input);
				}
			}
			else if (*input == 'j') // jnz
			{
				inst.op = VM::op_type::jnz;
				input += 4; // skip "jnz "
				if (*input >= 'a' && *input <= 'z')
				{
					inst.reg1 = *input;
					input++;
				}
				else
				{
					inst.value1 = numericParse<int>(input);
				}
				input++;
				if (*input >= 'a' && *input <= 'z')
				{
					inst.reg2 = *input;
					input++;
				}
				else
				{
					inst.value2 = numericParse<int>(input);
				}
			}

			instructions.push_back(inst);

			input++; // skip '\n'
		}

		// part 1
		VM p1_vm{ instructions };
		p1_vm.run();
		part1 = p1_vm.mul_count;

		// part 2
		int b_value = instructions[0].value2;
		b_value *= 100;
		b_value += 100000;
		int c_value = b_value;
		c_value += 17000;
		int h_value = 0;

		for (int b = b_value; b <= c_value; b += 17)
		{
			int f_value = 1;
			for (int d = 2; d < b; d++)
			{
				if (b % d == 0)
				{
					f_value = 0;
					break;
				}
			}

			if (f_value == 0)
			{
				h_value++;
			}
		}

		part2 = h_value;

		return { part1, part2 };
	}
};
