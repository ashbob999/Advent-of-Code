#include "../aocHelper.h"

class Day02 : public BaseDay
{
public:
	Day02() : BaseDay("02") {}

	result_type solve() override
	{
		long long part1 = 0;
		long long part2 = 0;

		char p[25];

		while (*input != '\0')
		{
			int i1 = numericParse<int>(input);
			input++;
			int i2 = numericParse<int>(input);


			input++;

			char c = *input;
			input++;
			input++;
			input++;

			int pCount = 0;

			int i = 0;
			while (*input != '\n')
			{
				p[i] = *input;
				if (*input == c)
				{
					pCount++;
				}

				input++;
				i++;
			}

			p[i] = '\0';
			input++;

			part2 += (p[i1 - 1] == c) ^ (p[i2 - 1] == c);

			part1 += (i1 <= pCount && pCount <= i2);
		}

		return { part1, part2 };

	}
};
