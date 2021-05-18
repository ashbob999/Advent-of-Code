#include "../aocHelper.h"

enum class instruction_type : int
{
	nop = 0,
	jmp = 1,
	acc = 2
};

enum class stopped_type : int
{
	infinte_loop = 0,
	out_of_bounds = 1
};

struct VM
{
	vector<pair<instruction_type, int>> instructions;
	int accumulator = 0;
	int pc = 0;
	int* seen;
	int swap_index = -1;

	VM(char*& input)
	{
		while (*input != '\0')
		{
			instruction_type it;

			if (*input == 'n')
			{
				it = instruction_type::nop;
			}
			else if (*input == 'a')
			{
				it = instruction_type::acc;
			}
			else if (*input == 'j')
			{
				it = instruction_type::jmp;
			}

			input += 4;

			int sign = 0;
			if (*input == '+')
			{
				sign = 1;
			}
			else if (*input == '-')
			{
				sign = -1;
			}

			input++;

			int number = numericParse<int>(input);

			instructions.emplace_back(it, sign * number);

			input++;
		}

		seen = new int[instructions.size()]{};
	}

	stopped_type run()
	{
		while (true)
		{
			// check for out of bounds
			if (pc == instructions.size())
			{
				return stopped_type::out_of_bounds;
			}

			// check if instruction has been seen
			if (seen[pc])
			{
				return stopped_type::infinte_loop;
			}

			// get instruction
			auto& op = instructions[pc];
			auto code = op.first;

			if (swap_index == pc)
			{
				code = (instruction_type) ((int) code ^ 1);
			}

			// mark instruction as seen
			seen[pc] = 1;

			switch (code)
			{
				case instruction_type::nop:
				{
					pc++;
					break;
				}
				case instruction_type::jmp:
				{
					pc += op.second;
					break;
				}
				case instruction_type::acc:
				{
					accumulator += op.second;
					pc++;
					break;
				}
				default:
					break;
			}
		}
	}

	void reset()
	{
		accumulator = 0;
		pc = 0;
		fill(seen, seen + instructions.size(), 0);
		swap_index = -1;
	}

	~VM()
	{
		delete seen;
	}
};

class Day08 : public BaseDay
{
public:
	Day08() : BaseDay("08") {}

	result_type solve() override
	{
		long long part1 = 0, part2 = 0;

		// parse input
		VM vm(input);

		// part 1
		vm.run();

		part1 = vm.accumulator;

		// part 2
		for (int i = 0; i < vm.instructions.size(); i++)
		{
			if (vm.instructions[i].first != instruction_type::acc)
			{
				vm.reset();
				vm.swap_index = i;
				auto result = vm.run();

				if (result == stopped_type::out_of_bounds)
				{
					part2 = vm.accumulator;
					break;
				}
			}
		}

		return { part1, part2 };
	}
};
