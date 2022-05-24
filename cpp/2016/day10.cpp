#include "../aocHelper.h"

class Day10 : public BaseDay
{
public:
	Day10() : BaseDay("10") {}

	result_type solve() override
	{
		long long part1 = 0, part2 = 0;

		struct bot
		{
			bool is_low_output = false;
			int low_value = 0;
			bool is_high_output = false;
			int high_value = 0;
			array<int, 2> values{ 0, 0 };
			int value_count = 0;

			void add_value(int n)
			{
				if (value_count == 0)
				{
					values[0] = n;
				}
				else
				{
					if (values[0] > n)
					{
						values[1] = values[0];
						values[0] = n;
					}
					else
					{
						values[1] = n;
					}
				}
				value_count++;
			}
		};

		auto solve = [&](unordered_map<int, vector<int>> inputs, unordered_map<int, bot> bots, unordered_map<int, int>& output, bool has_target, array<int, 2> targets)
		{
			// add initial inputs
			for (auto& p : inputs)
			{
				for (auto& v : p.second)
				{
					bots[p.first].add_value(v);
				}
			}

			while (bots.size() > 0)
			{
				for (auto it = bots.begin(); it != bots.end();)
				{
					bot& b = it->second;

					if (b.value_count == 2)
					{
						if (has_target && b.values[0] == targets[0] && b.values[1] == targets[1])
						{
							return it->first;
						}

						// handle low
						if (b.is_low_output)
						{
							output[b.low_value] = b.values[0];
						}
						else
						{
							bots[b.low_value].add_value(b.values[0]);
						}

						// handle high
						if (b.is_high_output)
						{
							output[b.high_value] = b.values[1];
						}
						else
						{
							bots[b.high_value].add_value(b.values[1]);
						}

						it = bots.erase(it);
					}
					else
					{
						it++;
					}
				}
			}

			return 0;
		};

		unordered_map<int, vector<int>> inputs;
		unordered_map<int, bot> bots;
		array<int, 2> targets = { 17, 61 };

		// parse input
		while (*input != '\0')
		{
			if (*input == 'b') // bot
			{
				input += 4; // skip "bot "
				int bot_id = numericParse<int>(input);
				input += 14; // skip " gives low to "

				bot b;

				if (*input == 'o') // low output
				{
					b.is_low_output = true;
					input += 7; // skip "output "
				}
				else // low bot
				{
					b.is_low_output = false;
					input += 4; // skip "bot "
				}

				b.low_value = numericParse<int>(input);

				input += 13; // skip " and high to "

				if (*input == 'o') // high output
				{
					b.is_high_output = true;
					input += 7; // skip "output "
				}
				else // high bot
				{
					b.is_high_output = false;
					input += 4; // skip "bot "
				}

				b.high_value = numericParse<int>(input);

				bots[bot_id] = b;
			}
			else // value
			{
				input += 6; // skip "value "
				int value = numericParse<int>(input);
				input += 13; // skip " goes to bot "
				int bot_id = numericParse<int>(input);

				inputs[bot_id].push_back(value);
			}
			input++; // skip '\n'
		}

		// part 1
		unordered_map<int, int> p1_outputs;
		part1 = solve(inputs, bots, p1_outputs, true, targets);


		// part 2
		unordered_map<int, int> p2_outputs;
		solve(inputs, bots, p2_outputs, false, {});
		part2 = p2_outputs[0] * p2_outputs[1] * p2_outputs[2];

		return { part1, part2 };
	}
};
