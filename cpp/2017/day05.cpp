#include "../aocHelper.h"

class Day05 : public BaseDay
{
public:
	Day05() : BaseDay("05") {}

	result_type solve() override
	{
		long long part1 = 0, part2 = 0;

		vector<int> jumps;

		// parse input
		while (*input != '\0')
		{
			int n = numericParse<int>(input);
			jumps.push_back(n);
			input++;
		}

		// part 1
		vector<int> p1_jumps = jumps;

		int i = 0;

		while (true)
		{
			int offset = p1_jumps[i];
			p1_jumps[i]++;
			i += offset;
			part1++;
			if (i < 0 || i >= p1_jumps.size())
			{
				break;
			}
		}

		// part 2
		vector<int> p2_jumps = jumps;

		i = 0;

		while (true)
		{
			int offset = p2_jumps[i];
			if (offset >= 3)
			{
				p2_jumps[i]--;
			}
			else
			{
				p2_jumps[i]++;
			}
			i += offset;
			part2++;
			if (i < 0 || i >= p2_jumps.size())
			{
				break;
			}
		}

		return { part1, part2 };
	}
};
