#include "../aocHelper.h"

class Day13 : public BaseDay
{
public:
	Day13() : BaseDay("13") {}

	result_type solve() override
	{
		long long part1 = 0, part2 = 0;

		unordered_map<int, int> layers;

		// parse input
		while (*input != '\0')
		{
			int level = numericParse<int>(input);

			input += 2; // skip ": "

			int size = numericParse<int>(input);

			layers.insert({ level, size });

			input++; // skip '\n'
		}

		int max_layer = 0;
		for (auto& p : layers)
		{
			if (p.first > max_layer)
			{
				max_layer = p.first;
			}
		}

		max_layer++;

		auto move = [&max_layer, &layers](int start_time)
		{
			vector<int> hit;

			for (int i = 0; i < max_layer; i++)
			{
				if (layers.contains(i))
				{
					if ((start_time + i) % (2 * layers[i] - 2) == 0)
					{
						hit.push_back(i);
					}
				}
			}

			return hit;
		};

		auto check_hit = [&max_layer, &layers](int start_time)
		{
			for (int i = 0; i < max_layer; i++)
			{
				if (layers.contains(i))
				{
					if ((start_time + i) % (2 * layers[i] - 2) == 0)
					{
						return false;
					}
				}
			}

			return true;
		};

		// part 1
		vector<int> hits = move(0);
		for (auto& h : hits)
		{
			part1 += h * layers[h];
		}

		// part 2
		while (true)
		{
			if (check_hit(part2))
			{
				break;
			}
			part2++;
		}

		return { part1, part2 };
	}
};
