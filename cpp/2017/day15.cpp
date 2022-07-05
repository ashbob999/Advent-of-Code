#include "../aocHelper.h"

class Day15 : public BaseDay
{
public:
	Day15() : BaseDay("15") {}

	result_type solve() override
	{
		long long part1 = 0, part2 = 0;

		vector<long long> gens;

		// parse input
		while (*input != '\0')
		{
			input += 24; // skip "Generator X starts with "

			long long num = numericParse<long long>(input);
			gens.push_back(num);

			input++; // skip '\n'
		}

		// part 1
		auto gen_next_value = [](long long prev_value, long long factor)
		{
			return (prev_value * factor) % 2147483647;
		};

		auto count_pairs = [&gen_next_value](long long gen_a_start, long long gen_b_start, int iterations)
		{
			int matches = 0;

			long long value_a = gen_a_start;
			long long value_b = gen_b_start;

			for (int i = 0; i < iterations; i++)
			{
				value_a = gen_next_value(value_a, 16807);
				value_b = gen_next_value(value_b, 48271);

				if ((value_a & 0xffff) == (value_b & 0xffff))
				{
					matches++;
				}
			}

			return matches;
		};

		part1 = count_pairs(gens[0], gens[1], 40000000);

		// part 2
		auto gen_next_value_2 = [](long long prev_value, long long factor, long long div)
		{
			long long value = (prev_value * factor) % 2147483647;
			while (value % div != 0)
			{
				value = (value * factor) % 2147483647;
			}
			return value;
		};

		auto count_pairs_2 = [&gen_next_value_2](long long gen_a_start, long long gen_b_start, int iterations)
		{
			int matches = 0;

			long long value_a = gen_a_start;
			long long value_b = gen_b_start;

			for (int i = 0; i < iterations; i++)
			{
				value_a = gen_next_value_2(value_a, 16807, 4);
				value_b = gen_next_value_2(value_b, 48271, 8);

				if ((value_a & 0xffff) == (value_b & 0xffff))
				{
					matches++;
				}
			}

			return matches;
		};

		part2 = count_pairs_2(gens[0], gens[1], 5000000);

		return { part1, part2 };
	}
};
