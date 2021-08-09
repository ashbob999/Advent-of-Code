#include "../aocHelper.h"

class Day01 : public BaseDay
{
public:
	Day01() : BaseDay("01") {}

	result_type solve() override
	{
		int part1 = 0, part2 = 0;

		int floor = 0;
		int count = 0;

		while (*input != '\0')
		{
			count++;

			if (*input == '(')
			{
				floor++;
			}
			else
			{
				floor--;
			}

			if (floor == -1 && part2 == 0)
			{
				part2 = count;
			}

			input++;
		}

		part1 = floor;

		return { part1, part2 };
	}
};
