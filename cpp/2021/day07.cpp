#include "../aocHelper.h"

class Day07 : public BaseDay
{
public:
	Day07() : BaseDay("07") {}

	result_type solve() override
	{
		long long part1 = 0, part2 = 0;

		vector<int> data;

		while (*input != '\0')
		{
			int n = numericParse<int>(input);
			data.push_back(n);
			input++;
		}

		// part 1
		auto solve_p1 = [&]()
		{
			int min_value = *min_element(data.begin(), data.end());
			int max_value = *max_element(data.begin(), data.end());

			int min_diff = INT_MAX;

			for (int hor_pos = min_value; hor_pos <= max_value; hor_pos++)
			{
				int diff = 0;
				for (auto& v : data)
				{
					diff += abs(hor_pos - v);
				}

				min_diff = min(min_diff, diff);
			}

			return min_diff;
		};

		part1 = solve_p1();

		// part 2
		auto linear_sum = [](int n)
		{
			return (n * (n - 1)) / 2;
		};

		auto solve_p2 = [&]()
		{
			int min_value = *min_element(data.begin(), data.end());
			int max_value = *max_element(data.begin(), data.end());

			int min_diff = INT_MAX;

			for (int hor_pos = min_value; hor_pos <= max_value; hor_pos++)
			{
				int diff = 0;
				for (auto& v : data)
				{
					diff += linear_sum(abs(hor_pos - v) + 1);
				}

				min_diff = min(min_diff, diff);
			}

			return min_diff;
		};

		part2 = solve_p2();

		return { part1, part2 };
	}
};
