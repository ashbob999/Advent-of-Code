#include "../aocHelper.h"

class Day05 : public BaseDay
{
public:
	Day05() : BaseDay("05") {}

	result_type solve() override
	{
		long long part1 = 0, part2 = 0;

		unsigned rowCheck = 0x100;

		// F -> 0
		// B -> 1
		// L -> 0
		// R -> 1

		vector<int> numbers;

		while (*input != '\0')
		{
			int number = 0;

			for (int r = 0; r < 7; r++)
			{
				number <<= 1;
				if (*input == 'B')
				{
					number |= 1;
				}
				input++;
			}

			for (int c = 0; c < 3; c++)
			{
				number <<= 1;
				if (*input == 'R')
				{
					number |= 1;
				}
				input++;
			}

			numbers.push_back(number);

			input++;
		}

		sort(numbers.begin(), numbers.end());

		part1 = numbers.back();

		for (int i = 0; i < numbers.size() - 1; i++)
		{
			if (numbers[i + 1] - numbers[i] == 2)
			{
				part2 = numbers[i] + 1;
				break;
			}
		}

		return { part1, part2 };
	}
};
