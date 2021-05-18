#include "../aocHelper.h"

class Day15 : public BaseDay
{
public:
	Day15() : BaseDay("15") {}

	result_type solve() override
	{
		long long part1 = 0, part2 = 0;

		vector<int> data;

		while (*input != '\0')
		{
			int n = numericParse<int>(input);
			data.push_back(n);
		}

		auto solve = [&data](long long target)
		{
			long long* prev = new long long[target + 1]();

			long long last = 1;
			long long num;

			for (long long i = 1; i < target + 1; i++)
			{
				if (i - 1 < data.size())
				{
					num = data[i - 1];
				}
				else if (prev[last] == 0)
				{
					num = 0;
				}
				else
				{
					num = i - prev[last];
				}

				prev[last] = i;
				last = num;
			}

			delete[] prev;

			return num;
		};

		part1 = solve(2020);
		part2 = solve(30'000'000);

		return { part1, part2 };
	}
};
