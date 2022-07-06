#include "../aocHelper.h"

class Day17 : public BaseDay
{
public:
	Day17() : BaseDay("17") {}

	result_type solve() override
	{
		long long part1 = 0, part2 = 0;

		// parse input
		int steps = numericParse<int>(input);

		// part 1
		auto get_buffer = [](int steps, int times)
		{
			vector<int> buffer = { 0 };
			int index = 0;

			for (int i = 1; i <= times; i++)
			{
				index = (index + steps) % buffer.size() + 1;
				buffer.insert(buffer.begin() + index, i);
			}

			return buffer;
		};

		vector<int> buffer = get_buffer(steps, 2017);
		int index = 0;
		for (int i = 0; i < buffer.size(); i++)
		{
			if (buffer[i] == 2017)
			{
				index = i;
				break;
			}
		}

		index = (index + 1) % buffer.size();

		part1 = buffer[index];

		// part 2
		auto get_value_after_0_in_buffer = [](int steps, int times)
		{
			int index = 0;
			int last_value_in_pos_1 = -1;

			for (int i = 1; i <= times; i++)
			{
				index = (index + steps) % i + 1;
				if (index == 1)
				{
					last_value_in_pos_1 = i;
				}
			}

			return last_value_in_pos_1;
		};

		part2 = get_value_after_0_in_buffer(steps, 50'000'000);

		return { part1, part2 };
	}
};
