#include "../aocHelper.h"

class Day01 : public BaseDay
{
public:
	Day01() : BaseDay("01") {}

	result_type solve() override
	{
		unordered_set<int> values;
		int part1 = 0, part2 = 0;

		int n;
		while ((n = numericParse<int>(input)))
		{
			values.insert(n);
		}

		set<int> sorted(values.begin(), values.end());

		// part 1
		for (auto& v : sorted)
		{
			int rem = 2020 - v;
			if (values.count(rem))
			{
				part1 = v * rem;
				break;
			}
		}

		// part2
		for (auto i = sorted.begin(); i != sorted.end(); i++)
		{
			for (auto j = next(i); j != sorted.end(); j++)
			{
				int rem = 2020 - *i - *j;
				if (values.count(rem))
				{
					part2 = rem * *i * *j;
					goto Done;
				}
			}
		}

	Done:
		return { part1, part2 };
	}
};
