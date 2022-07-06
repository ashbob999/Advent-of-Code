#include "../aocHelper.h"

struct VM_18_data
{
	enum class op_type
	{
		snd,
		set,
		add,
		mul,
		mod,
		rcv,
		jgz,
	};

	struct instr
	{
		op_type op;
		char reg1 = '\0';
		int value1 = 0;
		char reg2 = '\0';
		int value2 = 0;
	};
};

template<int type>
class VM_18
{
public:
	vector<VM_18_data::instr>& instructions;
	int id = 0;
	int pc = 0;
	unordered_map<char, long long> registers;
	bool finished = false;
	vector<int> played_sounds;
	int send_count = 0;
	deque<int> inputs;
	vector<int> outputs;

public:
	VM_18(vector<VM_18_data::instr>& instructions) : instructions(instructions)
	{
		static_assert(type == 0, "Use Other Constructor");

		for (int i = 'a'; i <= 'z'; i++)
		{
			registers[(char) i] = 0;
		}
	}

	VM_18(vector<VM_18_data::instr>& instructions, int id) : instructions(instructions)
	{
		static_assert(type == 1, "Use Other Constructor");
		this->id = id;

		for (int i = 'a'; i <= 'z'; i++)
		{
			registers[(char) i] = 0;
		}

		registers['p'] = id;
	}

	void run()
	{
		while (pc >= 0 && pc < instructions.size())
		{
			VM_18_data::instr& inst = instructions[pc];

			switch (inst.op)
			{
				case VM_18_data::op_type::snd:
				{
					if constexpr (type == 0)
					{
						played_sounds.push_back(registers[inst.reg1]);
					}
					else
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

						outputs.push_back(value);
						send_count++;
					}

					pc++;
					break;
				}
				case VM_18_data::op_type::set:
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
				case VM_18_data::op_type::add:
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

					registers[inst.reg1] += value;

					pc++;
					break;
				}
				case VM_18_data::op_type::mul:
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

					pc++;
					break;
				}
				case VM_18_data::op_type::mod:
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

					registers[inst.reg1] %= value;

					pc++;
					break;
				}
				case VM_18_data::op_type::rcv:
				{
					if constexpr (type == 0)
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

						if (value != 0)
						{
							return;
						}
					}
					else
					{
						if (inputs.size() > 0)
						{
							registers[inst.reg1] = inputs.front();
							inputs.pop_front();
						}
						else
						{
							return;
						}
					}

					pc++;
					break;
				}
				case VM_18_data::op_type::jgz:
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

					if (value > 0)
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

		finished = true;
	}

	void add_inputs(vector<int>& inputs)
	{
		static_assert(type == 1, "Function Only Allowed For Type 1");

		this->inputs.insert(this->inputs.end(), inputs.begin(), inputs.end());
		if (!finished)
		{
			run();
		}
	}
};

class Day18 : public BaseDay
{
public:
	Day18() : BaseDay("18") {}

	result_type solve() override
	{
		long long part1 = 0, part2 = 0;

		vector<VM_18_data::instr> instructions;

		// parse input
		while (*input != '\0')
		{
			VM_18_data::instr inst;

			if (*input == 's')
			{
				input++; // skip 's'

				if (*input == 'n') // snd X
				{
					inst.op = VM_18_data::op_type::snd;
					input += 3; // skip "nd "
					inst.reg1 = *input;
					input++;
				}
				else // set X Y
				{
					inst.op = VM_18_data::op_type::set;
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
			}
			else if (*input == 'm')
			{
				input++; // skip 'm'
				if (*input == 'u') // mul X Y
				{
					inst.op = VM_18_data::op_type::mul;
					input += 3; // skip "ul "
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
				else // mod X Y
				{
					inst.op = VM_18_data::op_type::mod;
					input += 3; // skip "od "
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
			else if (*input == 'a') // add X Y
			{
				inst.op = VM_18_data::op_type::add;
				input += 4; // skip "add "
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
			else if (*input == 'r') // rcv X
			{
				inst.op = VM_18_data::op_type::rcv;
				input += 4; // skip "rcv "
				inst.reg1 = *input;
				input++;
			}
			else if (*input == 'j') // jgz X Y
			{
				inst.op = VM_18_data::op_type::jgz;
				input += 4; // skip "jgz "
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
		VM_18<0> p1_vm{ instructions };
		p1_vm.run();
		part1 = p1_vm.played_sounds.back();

		// part 2
		VM_18<1> vm_0{ instructions, 0 };
		VM_18<1> vm_1{ instructions, 1 };

		while (!vm_0.finished || !vm_1.finished)
		{
			vm_0.run();
			vm_1.run();

			if (vm_0.outputs.size() == 0 && vm_1.outputs.size() == 0)
			{
				break;
			}

			vector<int> vm_0_out = vm_0.outputs;
			vm_0.outputs = {};

			vector<int> vm_1_out = vm_1.outputs;
			vm_1.outputs = {};

			vm_0.add_inputs(vm_1_out);
			vm_1.add_inputs(vm_0_out);
		}

		part2 = vm_1.send_count;

		return { part1, part2 };
	}
};
