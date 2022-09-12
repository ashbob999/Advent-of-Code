#include "../aocHelper.h"

class Day01 : public BaseDay
{
public:
	Day01() : BaseDay("01") {}

	result_type solve() override
	{
		long long part1 = 0, part2 = 0;

		vector<int> depths;

		while (*input != '\0')
		{
			int n = numericParse<int>(input);
			depths.push_back(n);
			input++; // skip '\n'
		}

		// part 1
		for (int i = 0; i < depths.size() - 1; i++)
		{
			if (depths[i] < depths[i + 1])
			{
				part1++;
			}
		}

		// part 2
		for (int i = 0; i < depths.size() - 3; i++)
		{
			if (depths[i] < depths[i + 3])
			{
				part2++;
			}
		}

		return { part1, part2 };
	}
};
