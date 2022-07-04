#include "../aocHelper.h"

class Day01 : public BaseDay
{
public:
	Day01() : BaseDay("01") {}

	result_type solve() override
	{
		long long part1 = 0, part2 = 0;

		vector<int> numbers;

		// parse input
		while (*input != '\n')
		{
			numbers.push_back(*input - '0');
			input++;
		}

		// part 1
		for (int i = 0; i < numbers.size(); i++)
		{
			if (numbers[i] == numbers[(i + 1) % numbers.size()])
			{
				part1 += numbers[i];
			}
		}

		// part 2
		for (int i = 0; i < numbers.size(); i++)
		{
			if (numbers[i] == numbers[(i + numbers.size() / 2) % numbers.size()])
			{
				part2 += numbers[i];
			}
		}

		return { part1, part2 };
	}
};
