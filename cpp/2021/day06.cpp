#include "../aocHelper.h"

class Day06 : public BaseDay
{
public:
	Day06() : BaseDay("06") {}

	result_type solve() override
	{
		long long part1 = 0, part2 = 0;

		vector<int> input_fish;

		while (*input != '\0')
		{
			int n = numericParse<int>(input);
			input_fish.push_back(n);
			input++;
		}

		array<long long, 9> fish_gens{};

		for (auto& f : input_fish)
		{
			fish_gens[f]++;
		}

		auto calc_gen = [&fish_gens]()
		{
			long long first = fish_gens[0];

			// shift all left
			shift_left(fish_gens.begin(), fish_gens.end(), 1);
			fish_gens[8] = first;

			fish_gens[6] += fish_gens[8];
		};

		// part 1
		int i = 0;
		for (; i < 80; i++)
		{
			calc_gen();
		}

		for (auto& v : fish_gens)
		{
			part1 += v;
		}

		// part 2
		for (; i < 256; i++)
		{
			calc_gen();
		}

		for (auto& v : fish_gens)
		{
			part2 += v;
		}

		return { part1, part2 };
	}
};
