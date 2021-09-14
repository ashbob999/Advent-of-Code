#include "../aocHelper.h"

class Day17 : public BaseDay
{
public:
	Day17() : BaseDay("17") {}

	result_type solve() override
	{
		long long part1 = 0, part2 = 0;

		vector<int> containers;

		// parse input
		while (*input != '\0')
		{
			int n = numericParse<int>(input);
			containers.push_back(n);

			input++; // skip \n
		}

		// sort containers, largest first
		sort(containers.begin(), containers.end(), greater<int>());

		function<int(int, int, int, int, int)> count;
		count = [&containers, &count](int s, int i, int max_sum, int used_conts, int max_conts)
		{
			int cnt = 0;

			if (i >= containers.size())
			{
				return 0;
			}

			cnt += count(s, i + 1, max_sum, used_conts, max_conts);

			if (used_conts < max_conts)
			{
				if (s + containers[i] < max_sum)
				{
					cnt += count(s + containers[i], i + 1, max_sum, used_conts + 1, max_conts);
				}
				else if (s + containers[i] == max_sum)
				{
					cnt++;
				}
			}

			return cnt;
		};

		function<int(int, int, int, int)> min_count;
		min_count = [&containers, &min_count](int s, int i, int max_sum, int used_conts)
		{
			int min_used = 100'000'000;

			if (i >= containers.size())
			{
				return 100'000'000;
			}

			min_used = min(min_count(s, i + 1, max_sum, used_conts), min_used);

			if (s + containers[i] < max_sum)
			{
				min_used = min(min_count(s + containers[i], i + 1, max_sum, used_conts + 1), min_used);
			}
			else if (s + containers[i] == max_sum)
			{
				min_used = min(min_used, used_conts + 1);
			}

			return min_used;
		};

		constexpr int amount = 150;

		// part 1
		part1 = count(0, 0, amount, 0, containers.size());

		// part 2
		int min_amount = min_count(0, 0, amount, 0);
		part2 = count(0, 0, amount, 0, min_amount);

		return { part1, part2 };
	}
};
